Finding tests in all modules
============================

Normally, nose only looks for tests in modules whose names match testMatch. By
default that means modules with 'test' or 'Test' at the start of the name
after an underscore (_) or dash (-) or other non-alphanumeric character.

If you want to collect tests from all modules, use the ``--all-modules``
command line argument to activate the :doc:`allmodules plugin
<../../plugins/allmodules>`.

.. Note ::

   The function :func:`nose.plugins.plugintest.run` reformats test result
   output to remove timings, which will vary from run to run, and
   redirects the output to stdout.

    >>> from nose.plugins.plugintest import run_buffered as run

..

    >>> import os
    >>> support = os.path.join(os.path.dirname(__file__), 'support')
    >>> argv = [__file__, '-v', support]

The target directory contains a test module and a normal module.

    >>> support_files = [d for d in os.listdir(support)
    ...                  if not d.startswith('.')
    ...                  and d.endswith('.py')]
    >>> support_files.sort()
    >>> support_files
    ['mod.py', 'test.py']

When run without ``--all-modules``, only the test module is examined for tests.

    >>> run(argv=argv)
    test.test ... ok
    <BLANKLINE>
    ----------------------------------------------------------------------
    Ran 1 test in ...s
    <BLANKLINE>
    OK

When ``--all-modules`` is active, both modules are examined.

    >>> from nose.plugins.allmodules import AllModules
    >>> argv = [__file__, '-v', '--all-modules', support]
    >>> run(argv=argv, plugins=[AllModules()]) # doctest: +REPORT_NDIFF
    mod.test ... ok
    mod.test_fails ... FAIL
    test.test ... ok
    <BLANKLINE>
    ======================================================================
    FAIL: mod.test_fails
    ----------------------------------------------------------------------
    Traceback (most recent call last):
    ...
    AssertionError: This test fails
    <BLANKLINE>
    ----------------------------------------------------------------------
    Ran 3 tests in ...s
    <BLANKLINE>
    FAILED (failures=1)



