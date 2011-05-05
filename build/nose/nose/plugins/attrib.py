"""Attribute selector plugin.

Oftentimes when testing you will want to select tests based on
criteria rather then simply by filename. For example, you might want
to run all tests except for the slow ones. You can do this with the
Attribute selector plugin by setting attributes on your test methods.
Here is an example:

.. code-block:: python

    def test_big_download():
        import urllib
        # commence slowness...

    test_big_download.slow = 1

Once you've assigned an attribute ``slow = 1`` you can exclude that
test and all other tests having the slow attribute by running ::

    $ nosetests -a '!slow'

There is also a decorator available for you that will set attributes.
Here's how to set ``slow=1`` like above with the decorator:

.. code-block:: python

    from nose.plugins.attrib import attr
    @attr('slow')
    def test_big_download():
        import urllib
        # commence slowness...

And here's how to set an attribute with a specific value:

.. code-block:: python

    from nose.plugins.attrib import attr
    @attr(speed='slow')
    def test_big_download():
        import urllib
        # commence slowness...

This test could be run with ::

    $ nosetests -a speed=slow

Below is a reference to the different syntaxes available.

Simple syntax
-------------

Examples of using the ``-a`` and ``--attr`` options:

* ``nosetests -a status=stable``
   Only runs tests with attribute "status" having value "stable"

* ``nosetests -a priority=2,status=stable``
   Runs tests having both attributes and values

* ``nosetests -a priority=2 -a slow``
   Runs tests that match either attribute

* ``nosetests -a tags=http``
   If a test's ``tags`` attribute was a list and it contained the value
   ``http`` then it would be run

* ``nosetests -a slow``
   Runs tests with the attribute ``slow`` if its value does not equal False
   (False, [], "", etc...)

* ``nosetests -a '!slow'``
   Runs tests that do NOT have the attribute ``slow`` or have a ``slow``
   attribute that is equal to False
   **NOTE**:
   if your shell (like bash) interprets '!' as a special character make sure to
   put single quotes around it.

Expression Evaluation
---------------------

Examples using the ``-A`` and ``--eval-attr`` options:

* ``nosetests -A "not slow"``
  Evaluates the Python expression "not slow" and runs the test if True

* ``nosetests -A "(priority > 5) and not slow"``
  Evaluates a complex Python expression and runs the test if True

"""
import logging
import os
import sys
from inspect import isfunction
from nose.plugins.base import Plugin
from nose.util import tolist

log = logging.getLogger('nose.plugins.attrib')
compat_24 = sys.version_info >= (2, 4)

def attr(*args, **kwargs):
    """Decorator that adds attributes to objects
    for use with the Attribute (-a) plugin.
    """
    def wrap(func):
        for name in args:
            # these are just True flags:
            setattr(func, name, 1)
        func.__dict__.update(kwargs)
        return func
    return wrap

class ContextHelper:
    """Returns default values for dictionary lookups."""
    def __init__(self, obj):
        self.obj = obj

    def __getitem__(self, name):
        return self.obj.get(name, False)


class AttributeGetter:
    """Helper for looking up attributes

    First we check the method, and if the attribute is not present,
    we check the method's class.
    """
    missing = object()

    def __init__(self, cls, method):
        self.cls = cls
        self.method = method

    def get(self, name, default=None):
        log.debug('Get %s from %s.%s', name, self.cls, self.method)
        val = self.method.__dict__.get(name, self.missing)
        if val is self.missing:
            log.debug('No attribute %s in method, getting from class',
                      name)
            val = getattr(self.cls, name, default)
            log.debug('Class attribute %s value: %s', name, val)
        return val

class AttributeSelector(Plugin):
    """Selects test cases to be run based on their attributes.
    """

    def __init__(self):
        Plugin.__init__(self)
        self.attribs = []

    def options(self, parser, env):
        """Register command line options"""
        parser.add_option("-a", "--attr",
                          dest="attr", action="append",
                          default=env.get('NOSE_ATTR'),
                          metavar="ATTR",
                          help="Run only tests that have attributes "
                          "specified by ATTR [NOSE_ATTR]")
        # disable in < 2.4: eval can't take needed args
        if compat_24:
            parser.add_option("-A", "--eval-attr",
                              dest="eval_attr", metavar="EXPR", action="append",
                              default=env.get('NOSE_EVAL_ATTR'),
                              help="Run only tests for whose attributes "
                              "the Python expression EXPR evaluates "
                              "to True [NOSE_EVAL_ATTR]")

    def configure(self, options, config):
        """Configure the plugin and system, based on selected options.

        attr and eval_attr may each be lists.

        self.attribs will be a list of lists of tuples. In that list, each
        list is a group of attributes, all of which must match for the rule to
        match.
        """
        self.attribs = []

        # handle python eval-expression parameter
        if compat_24 and options.eval_attr:
            eval_attr = tolist(options.eval_attr)
            for attr in eval_attr:
                # "<python expression>"
                # -> eval(expr) in attribute context must be True
                def eval_in_context(expr, attribs):
                    return eval(expr, None, ContextHelper(attribs))
                self.attribs.append([(attr, eval_in_context)])

        # attribute requirements are a comma separated list of
        # 'key=value' pairs
        if options.attr:
            std_attr = tolist(options.attr)
            for attr in std_attr:
                # all attributes within an attribute group must match
                attr_group = []
                for attrib in attr.strip().split(","):
                    # don't die on trailing comma
                    if not attrib:
                        continue
                    items = attrib.split("=", 1)
                    if len(items) > 1:
                        # "name=value"
                        # -> 'str(obj.name) == value' must be True
                        key, value = items
                    else:
                        key = items[0]
                        if key[0] == "!":
                            # "!name"
                            # 'bool(obj.name)' must be False
                            key = key[1:]
                            value = False
                        else:
                            # "name"
                            # -> 'bool(obj.name)' must be True
                            value = True
                    attr_group.append((key, value))
                self.attribs.append(attr_group)
        if self.attribs:
            self.enabled = True

    def validateAttrib(self, attribs):
        # TODO: is there a need for case-sensitive value comparison?
        # within each group, all must match for the group to match
        # if any group matches, then the attribute set as a whole
        # has matched
        any = False
        for group in self.attribs:
            match = True
            for key, value in group:
                obj_value = attribs.get(key)
                if callable(value):
                    if not value(key, attribs):
                        match = False
                        break
                elif value is True:
                    # value must exist and be True
                    if not bool(obj_value):
                        match = False
                        break
                elif value is False:
                    # value must not exist or be False
                    if bool(obj_value):
                        match = False
                        break
                elif type(obj_value) in (list, tuple):
                    # value must be found in the list attribute

                    if not str(value).lower() in [str(x).lower()
                                                  for x in obj_value]:
                        match = False
                        break
                else:
                    # value must match, convert to string and compare
                    if (value != obj_value
                        and str(value).lower() != str(obj_value).lower()):
                        match = False
                        break
            any = any or match
        if any:
            # not True because we don't want to FORCE the selection of the
            # item, only say that it is acceptable
            return None
        return False

    def wantClass(self, cls):
        """Accept the class if the class or any method is wanted.
        """
        cls_attr = cls.__dict__
        if self.validateAttrib(cls_attr) is not False:
            return None
        # Methods in __dict__.values() are functions, oddly enough.
        methods = filter(isfunction, cls_attr.values())
        wanted = filter(lambda m: m is not False,
                        map(self.wantFunction, methods))
        if wanted:
            return None
        return False

    def wantFunction(self, function):
        """Accept the function if its attributes match.
        """
        return self.validateAttrib(function.__dict__)

    def wantMethod(self, method):
        """Accept the method if its attributes match.
        """
        attribs = AttributeGetter(method.im_class, method)
        return self.validateAttrib(attribs)
