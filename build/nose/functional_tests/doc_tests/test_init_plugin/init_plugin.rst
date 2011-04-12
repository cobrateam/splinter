Running Initialization Code Before the Test Run
-----------------------------------------------

Many applications, especially those using web frameworks like Pylons_
or Django_, can't be tested without first being configured or
otherwise initialized. Plugins can fulfill this requirement by
implementing `begin()`_.

In this example, we'll use a very simple example: a widget class that
can't be tested without a configuration.

Here's the widget class. It's configured at the class or instance
level by setting the ``cfg`` attribute to a dictionary.

    >>> class ConfigurableWidget(object):
    ...     cfg = None
    ...     def can_frobnicate(self):
    ...         return self.cfg.get('can_frobnicate', True)
    ...     def likes_cheese(self):
    ...         return self.cfg.get('likes_cheese', True)

The tests verify that the widget's methods can be called without
raising any exceptions.

    >>> import unittest
    >>> class TestConfigurableWidget(unittest.TestCase):
    ...     longMessage = False
    ...     def setUp(self):
    ...         self.widget = ConfigurableWidget()
    ...     def test_can_frobnicate(self):
    ...         """Widgets can frobnicate (or not)"""
    ...         self.widget.can_frobnicate()
    ...     def test_likes_cheese(self):
    ...         """Widgets might like cheese"""
    ...         self.widget.likes_cheese()
    ...     def shortDescription(self): # 2.7 compat
    ...         try:
    ...             doc = self._testMethodDoc
    ...         except AttributeError:
    ...             # 2.4 compat
    ...             doc = self._TestCase__testMethodDoc
    ...         return doc and doc.split("\n")[0].strip() or None

The tests are bundled into a suite that we can pass to the test runner.

    >>> def suite():
    ...     return unittest.TestSuite([
    ...         TestConfigurableWidget('test_can_frobnicate'),
    ...         TestConfigurableWidget('test_likes_cheese')])

When we run tests without first configuring the ConfigurableWidget,
the tests fail.

.. Note ::

   The function :func:`nose.plugins.plugintest.run` reformats test result
   output to remove timings, which will vary from run to run, and
   redirects the output to stdout.

    >>> from nose.plugins.plugintest import run_buffered as run

..

    >>> argv = [__file__, '-v']
    >>> run(argv=argv, suite=suite())  # doctest: +REPORT_NDIFF
    Widgets can frobnicate (or not) ... ERROR
    Widgets might like cheese ... ERROR
    <BLANKLINE>
    ======================================================================
    ERROR: Widgets can frobnicate (or not)
    ----------------------------------------------------------------------
    Traceback (most recent call last):
    ...
    AttributeError: 'NoneType' object has no attribute 'get'
    <BLANKLINE>
    ======================================================================
    ERROR: Widgets might like cheese
    ----------------------------------------------------------------------
    Traceback (most recent call last):
    ...
    AttributeError: 'NoneType' object has no attribute 'get'
    <BLANKLINE>
    ----------------------------------------------------------------------
    Ran 2 tests in ...s
    <BLANKLINE>
    FAILED (errors=2)

To configure the widget system before running tests, write a plugin
that implements `begin()`_ and initializes the system with a
hard-coded configuration. (Later, we'll write a better plugin that
accepts a command-line argument specifying the configuration file.)

    >>> from nose.plugins import Plugin
    >>> class ConfiguringPlugin(Plugin):
    ...     enabled = True
    ...     def configure(self, options, conf):
    ...         pass # always on
    ...     def begin(self):
    ...         ConfigurableWidget.cfg = {}

Now configure and execute a new test run using the plugin, which will
inject the hard-coded configuration.

    >>> run(argv=argv, suite=suite(),
    ...     plugins=[ConfiguringPlugin()])  # doctest: +REPORT_NDIFF
    Widgets can frobnicate (or not) ... ok
    Widgets might like cheese ... ok
    <BLANKLINE>
    ----------------------------------------------------------------------
    Ran 2 tests in ...s
    <BLANKLINE>
    OK

This time the tests pass, because the widget class is configured.

But the ConfiguringPlugin is pretty lame -- the configuration it
installs is hard coded. A better plugin would allow the user to
specify a configuration file on the command line:

    >>> class BetterConfiguringPlugin(Plugin):
    ...     def options(self, parser, env={}):
    ...         parser.add_option('--widget-config', action='store',
    ...                           dest='widget_config', default=None,
    ...                           help='Specify path to widget config file')
    ...     def configure(self, options, conf):
    ...         if options.widget_config:
    ...             self.load_config(options.widget_config)
    ...             self.enabled = True
    ...     def begin(self):
    ...         ConfigurableWidget.cfg = self.cfg
    ...     def load_config(self, path):
    ...         from ConfigParser import ConfigParser
    ...         p = ConfigParser()
    ...         p.read([path])
    ...         self.cfg = dict(p.items('DEFAULT'))

To use the plugin, we need a config file.

    >>> import os
    >>> cfg_file = os.path.join(os.path.dirname(__file__), 'example.cfg')
    >>> open(cfg_file, 'w').write("""\
    ... [DEFAULT]
    ... can_frobnicate = 1
    ... likes_cheese = 0
    ... """)

Now we can execute a test run using that configuration, after first
resetting the widget system to an unconfigured state.

    >>> ConfigurableWidget.cfg = None
    >>> argv = [__file__, '-v', '--widget-config', cfg_file]
    >>> run(argv=argv, suite=suite(),
    ...     plugins=[BetterConfiguringPlugin()]) # doctest: +REPORT_NDIFF
    Widgets can frobnicate (or not) ... ok
    Widgets might like cheese ... ok
    <BLANKLINE>
    ----------------------------------------------------------------------
    Ran 2 tests in ...s
    <BLANKLINE>
    OK

.. _Pylons: http://pylonshq.com/
.. _Django: http://www.djangoproject.com/
.. _`begin()`: plugin_interface.html#begin
