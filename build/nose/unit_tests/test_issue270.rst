Multiprocess test collection from packages
------------------------------------------

Tests that the multiprocess plugin correctly collects tests from packages

    >>> import os
    >>> from nose.plugins.plugintest import run_buffered as run
    >>> from nose.plugins.multiprocess import MultiProcess
    >>> support = os.path.join(os.path.dirname(__file__), 'support')
    >>> issue270 = os.path.join(support, 'issue270')

The test package has a package-level fixture, which causes the entire package
to be dispatched to a multiprocess worker. Tests are still collected and run
properly.

    >>> argv = [__file__, '-v', '--processes=2', issue270]
    >>> run(argv=argv, plugins=[MultiProcess()])
    issue270.foo_test.Foo_Test.test_bar ... ok
    issue270.foo_test.Foo_Test.test_foo ... ok
    <BLANKLINE>
    ----------------------------------------------------------------------
    Ran 2 tests in ...s
    <BLANKLINE>
    OK
