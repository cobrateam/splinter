Restricted Plugin Managers
--------------------------

In some cases, such as running under the ``python setup.py test`` command,
nose is not able to use all available plugins. In those cases, a
`nose.plugins.manager.RestrictedPluginManager` is used to exclude plugins that
implement API methods that nose is unable to call.

Support files for this test are in the support directory.

    >>> import os
    >>> support = os.path.join(os.path.dirname(__file__), 'support')

For this test, we'll use a simple plugin that implements the ``startTest``
method.

    >>> from nose.plugins.base import Plugin
    >>> from nose.plugins.manager import RestrictedPluginManager
    >>> class StartPlugin(Plugin):
    ...     def startTest(self, test):
    ...         print "started %s" % test

.. Note ::

   The run() function in :mod:`nose.plugins.plugintest` reformats test result
   output to remove timings, which will vary from run to run, and
   redirects the output to stdout.

    >>> from nose.plugins.plugintest import run_buffered as run

..

When run with a normal plugin manager, the plugin executes.

    >>> argv = ['plugintest', '-v', '--with-startplugin', support]
    >>> run(argv=argv, plugins=[StartPlugin()]) # doctest: +REPORT_NDIFF
    started test.test
    test.test ... ok
    <BLANKLINE>
    ----------------------------------------------------------------------
    Ran 1 test in ...s
    <BLANKLINE>
    OK

However, when run with a restricted plugin manager configured to exclude
plugins implementing `startTest`, an exception is raised and nose exits.

    >>> restricted = RestrictedPluginManager(
    ...     plugins=[StartPlugin()], exclude=('startTest',), load=False)
    >>> run(argv=argv, plugins=restricted) #doctest: +REPORT_NDIFF +ELLIPSIS
    Traceback (most recent call last):
    ...
    SystemExit: ...

Errors are only raised when options defined by excluded plugins are used.

    >>> argv = ['plugintest', '-v', support]
    >>> run(argv=argv, plugins=restricted) # doctest: +REPORT_NDIFF
    test.test ... ok
    <BLANKLINE>
    ----------------------------------------------------------------------
    Ran 1 test in ...s
    <BLANKLINE>
    OK

When a disabled option appears in a configuration file, instead of on the
command line, a warning is raised instead of an exception.

    >>> argv = ['plugintest', '-v', '-c', os.path.join(support, 'start.cfg'),
    ...         support]
    >>> run(argv=argv, plugins=restricted) # doctest: +ELLIPSIS
    RuntimeWarning: Option 'with-startplugin' in config file '...start.cfg' ignored: excluded by runtime environment
    test.test ... ok
    <BLANKLINE>
    ----------------------------------------------------------------------
    Ran 1 test in ...s
    <BLANKLINE>
    OK

However, if an option appears in a configuration file that is not recognized
either as an option defined by nose, or by an active or excluded plugin, an
error is raised.

    >>> argv = ['plugintest', '-v', '-c', os.path.join(support, 'bad.cfg'),
    ...         support]
    >>> run(argv=argv, plugins=restricted) # doctest: +ELLIPSIS
    Traceback (most recent call last):
    ...
    ConfigError: Error reading config file '...bad.cfg': no such option 'with-meltedcheese'
