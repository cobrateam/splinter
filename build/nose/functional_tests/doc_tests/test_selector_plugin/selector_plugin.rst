Using a Custom Selector
-----------------------

By default, nose uses a `nose.selector.Selector` instance to decide
what is and is not a test. The default selector is fairly simple: for
the most part, if an object's name matches the ``testMatch`` regular
expression defined in the active `nose.config.Config` instance, the
object is selected as a test. 

This behavior is fine for new projects, but may be undesireable for
older projects with a different test naming scheme. Fortunately, you
can easily override this behavior by providing a custom selector using
a plugin.

    >>> import os
    >>> support = os.path.join(os.path.dirname(__file__), 'support')

In this example, the project to be tested consists of a module and
package and associated tests, laid out like this::

    >>> from nose.util import ls_tree
    >>> print ls_tree(support)
    |-- mymodule.py
    |-- mypackage
    |   |-- __init__.py
    |   |-- strings.py
    |   `-- math
    |       |-- __init__.py
    |       `-- basic.py
    `-- tests
        |-- testlib.py
        |-- math
        |   `-- basic.py
        |-- mymodule
        |   `-- my_function.py
        `-- strings
            `-- cat.py

Because the test modules do not include ``test`` in their names,
nose's default selector is unable to discover this project's tests.

.. Note ::

   The run() function in :mod:`nose.plugins.plugintest` reformats test result
   output to remove timings, which will vary from run to run, and
   redirects the output to stdout.

    >>> from nose.plugins.plugintest import run_buffered as run

..

    >>> argv = [__file__, '-v', support]
    >>> run(argv=argv)
    ----------------------------------------------------------------------
    Ran 0 tests in ...s
    <BLANKLINE>
    OK

The tests for the example project follow a few basic conventions:

* The are all located under the tests/ directory.
* Test modules are organized into groups under directories named for
  the module or package they test.
* testlib is *not* a test module, but it must be importable by the
  test modules.
* Test modules contain unitest.TestCase classes that are tests, and
  may contain other functions or classes that are NOT tests, no matter
  how they are named.

We can codify those conventions in a selector class.

    >>> from nose.selector import Selector
    >>> import unittest
    >>> class MySelector(Selector):
    ...     def wantDirectory(self, dirname):
    ...         # we want the tests directory and all directories
    ...         # beneath it, and no others
    ...         parts = dirname.split(os.path.sep)
    ...         return 'tests' in parts
    ...     def wantFile(self, filename):
    ...         # we want python modules under tests/, except testlib
    ...         parts = filename.split(os.path.sep)
    ...         base, ext = os.path.splitext(parts[-1])
    ...         return 'tests' in parts and ext == '.py' and base != 'testlib'
    ...     def wantModule(self, module):
    ...         # wantDirectory and wantFile above will ensure that
    ...         # we never see an unwanted module
    ...         return True
    ...     def wantFunction(self, function):
    ...         # never collect functions
    ...         return False
    ...     def wantClass(self, cls):
    ...         # only collect TestCase subclasses
    ...         return issubclass(cls, unittest.TestCase)

To use our selector class, we need a plugin that can inject it into
the test loader.

    >>> from nose.plugins import Plugin
    >>> class UseMySelector(Plugin):
    ...     enabled = True
    ...     def configure(self, options, conf):
    ...         pass # always on
    ...     def prepareTestLoader(self, loader):
    ...         loader.selector = MySelector(loader.config)

Now we can execute a test run using the custom selector, and the
project's tests will be collected.

    >>> run(argv=argv, plugins=[UseMySelector()])
    test_add (basic.TestBasicMath) ... ok
    test_sub (basic.TestBasicMath) ... ok
    test_tuple_groups (my_function.MyFunction) ... ok
    test_cat (cat.StringsCat) ... ok
    <BLANKLINE>
    ----------------------------------------------------------------------
    Ran 4 tests in ...s
    <BLANKLINE>
    OK
