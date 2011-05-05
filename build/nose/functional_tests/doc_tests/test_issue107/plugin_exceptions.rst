When Plugins Fail
-----------------

Plugin methods should not fail silently. When a plugin method raises
an exception before or during the execution of a test, the exception
will be wrapped in a :class:`nose.failure.Failure` instance and appear as a
failing test. Exceptions raised at other times, such as in the
preparation phase with ``prepareTestLoader`` or ``prepareTestResult``,
or after a test executes, in ``afterTest`` will stop the entire test
run.

    >>> import os
    >>> import sys
    >>> from nose.plugins import Plugin
    >>> from nose.plugins.plugintest import run_buffered as run

Our first test plugins take no command-line arguments and raises
AttributeError in beforeTest and afterTest. 

    >>> class EnabledPlugin(Plugin):
    ...     """Plugin that takes no command-line arguments"""
    ...
    ...     enabled = True
    ...
    ...     def configure(self, options, conf):
    ...         pass
    ...     def options(self, parser, env={}):
    ...         pass    
    >>> class FailBeforePlugin(EnabledPlugin):
    ...     name = "fail-before"
    ...	    
    ...     def beforeTest(self, test):
    ...         raise AttributeError()    
    >>> class FailAfterPlugin(EnabledPlugin):
    ...     name = "fail-after"
    ...	    
    ...     def afterTest(self, test):
    ...         raise AttributeError()

Running tests with the fail-before plugin enabled will result in all
tests failing.

    >>> support = os.path.join(os.path.dirname(__file__), 'support')
    >>> suitepath = os.path.join(support, 'test_spam.py')
    >>> run(argv=['nosetests', suitepath],
    ...     plugins=[FailBeforePlugin()])
    EE
    ======================================================================
    ERROR: test_spam.test_spam
    ----------------------------------------------------------------------
    Traceback (most recent call last):
    ...
    AttributeError
    <BLANKLINE>
    ======================================================================
    ERROR: test_spam.test_eggs
    ----------------------------------------------------------------------
    Traceback (most recent call last):
    ...
    AttributeError
    <BLANKLINE>
    ----------------------------------------------------------------------
    Ran 0 tests in ...s
    <BLANKLINE>
    FAILED (errors=2)

But with the fail-after plugin, the entire test run will fail.

    >>> run(argv=['nosetests', suitepath],
    ...     plugins=[FailAfterPlugin()])
    Traceback (most recent call last):
    ...
    AttributeError

Likewise, since the next plugin fails in a preparatory method, outside
of test execution, the entire test run fails when the plugin is used.

    >>> class FailPreparationPlugin(EnabledPlugin):
    ...     name = "fail-prepare"
    ...     
    ...     def prepareTestLoader(self, loader):
    ...         raise TypeError("That loader is not my type")
    >>> run(argv=['nosetests', suitepath],
    ...     plugins=[FailPreparationPlugin()])
    Traceback (most recent call last):
    ...
    TypeError: That loader is not my type


Even AttributeErrors and TypeErrors are not silently suppressed as
they used to be for some generative plugin methods (issue152).

These methods caught TypeError and AttributeError and did not record
the exception, before issue152 was fixed: .loadTestsFromDir(),
.loadTestsFromModule(), .loadTestsFromTestCase(),
loadTestsFromTestClass, and .makeTest().  Now, the exception is
caught, but logged as a Failure.

    >>> class FailLoadPlugin(EnabledPlugin):
    ...     name = "fail-load"
    ...     
    ...     def loadTestsFromModule(self, module):
    ...         # we're testing exception handling behaviour during
    ...         # iteration, so be a generator function, without
    ...         # actually yielding any tests
    ...         if False:
    ...             yield None
    ...         raise TypeError("bug in plugin")
    >>> run(argv=['nosetests', suitepath],
    ...     plugins=[FailLoadPlugin()])
    ..E
    ======================================================================
    ERROR: Failure: TypeError (bug in plugin)
    ----------------------------------------------------------------------
    Traceback (most recent call last):
    ...
    TypeError: bug in plugin
    <BLANKLINE>
    ----------------------------------------------------------------------
    Ran 3 tests in ...s
    <BLANKLINE>
    FAILED (errors=1)


Also, before issue152 was resolved, .loadTestsFromFile() and
.loadTestsFromName() didn't catch these errors at all, so the
following test would crash nose:

    >>> class FailLoadFromNamePlugin(EnabledPlugin):
    ...     name = "fail-load-from-name"
    ...     
    ...     def loadTestsFromName(self, name, module=None, importPath=None):
    ...         if False:
    ...             yield None
    ...         raise TypeError("bug in plugin")
    >>> run(argv=['nosetests', suitepath],
    ...     plugins=[FailLoadFromNamePlugin()])
    E
    ======================================================================
    ERROR: Failure: TypeError (bug in plugin)
    ----------------------------------------------------------------------
    Traceback (most recent call last):
    ...
    TypeError: bug in plugin
    <BLANKLINE>
    ----------------------------------------------------------------------
    Ran 1 test in ...s
    <BLANKLINE>
    FAILED (errors=1)
