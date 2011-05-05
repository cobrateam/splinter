Failure of Errorclasses
-----------------------

Errorclasses (skips, deprecations, etc.) define whether or not they
represent test failures.

    >>> import os
    >>> import sys
    >>> from nose.plugins.plugintest import run_buffered as run
    >>> from nose.plugins.skip import Skip
    >>> from nose.plugins.deprecated import Deprecated
    >>> support = os.path.join(os.path.dirname(__file__), 'support')
    >>> sys.path.insert(0, support)
    >>> from errorclass_failure_plugin import Todo, TodoPlugin, \
    ...                                       NonFailureTodoPlugin
    >>> todo_test = os.path.join(support, 'errorclass_failing_test.py')
    >>> misc_test = os.path.join(support, 'errorclass_tests.py')

nose.plugins.errorclass.ErrorClass has an argument ``isfailure``. With a
true isfailure, when the errorclass' exception is raised by a test,
tracebacks are printed.

    >>> run(argv=["nosetests", "-v", "--with-todo", todo_test],
    ...     plugins=[TodoPlugin()])  # doctest: +REPORT_NDIFF
    errorclass_failing_test.test_todo ... TODO: fix me
    errorclass_failing_test.test_2 ... ok
    <BLANKLINE>
    ======================================================================
    TODO: errorclass_failing_test.test_todo
    ----------------------------------------------------------------------
    Traceback (most recent call last):
    ...
    Todo: fix me
    <BLANKLINE>
    ----------------------------------------------------------------------
    Ran 2 tests in ...s
    <BLANKLINE>
    FAILED (TODO=1)


Also, ``--stop`` stops the test run.

    >>> run(argv=["nosetests", "-v", "--with-todo", "--stop", todo_test],
    ...     plugins=[TodoPlugin()])  # doctest: +REPORT_NDIFF
    errorclass_failing_test.test_todo ... TODO: fix me
    <BLANKLINE>
    ======================================================================
    TODO: errorclass_failing_test.test_todo
    ----------------------------------------------------------------------
    Traceback (most recent call last):
    ...
    Todo: fix me
    <BLANKLINE>
    ----------------------------------------------------------------------
    Ran 1 test in ...s
    <BLANKLINE>
    FAILED (TODO=1)


With a false .isfailure, errorclass exceptions raised by tests are
treated as "ignored errors."  For ignored errors, tracebacks are not
printed, and the test run does not stop.

    >>> run(argv=["nosetests", "-v", "--with-non-failure-todo", "--stop",
    ...           todo_test],
    ...     plugins=[NonFailureTodoPlugin()])  # doctest: +REPORT_NDIFF
    errorclass_failing_test.test_todo ... TODO: fix me
    errorclass_failing_test.test_2 ... ok
    <BLANKLINE>
    ----------------------------------------------------------------------
    Ran 2 tests in ...s
    <BLANKLINE>
    OK (TODO=1)


Exception detail strings of errorclass errors are always printed when
-v is in effect, regardless of whether the error is ignored.  Note
that exception detail strings may have more than one line.

    >>> run(argv=["nosetests", "-v", "--with-todo", misc_test],
    ...     plugins=[TodoPlugin(), Skip(), Deprecated()])
    ... # doctest: +REPORT_NDIFF
    errorclass_tests.test_todo ... TODO: fix me
    errorclass_tests.test_2 ... ok
    errorclass_tests.test_3 ... SKIP: skipety-skip
    errorclass_tests.test_4 ... SKIP
    errorclass_tests.test_5 ... DEPRECATED: spam
    eggs
    <BLANKLINE>
    spam
    errorclass_tests.test_6 ... DEPRECATED: spam
    <BLANKLINE>
    ======================================================================
    TODO: errorclass_tests.test_todo
    ----------------------------------------------------------------------
    Traceback (most recent call last):
    ...
    Todo: fix me
    <BLANKLINE>
    ----------------------------------------------------------------------
    Ran 6 tests in ...s
    <BLANKLINE>
    FAILED (DEPRECATED=2, SKIP=2, TODO=1)

Without -v, the exception detail strings are only displayed if the
error is not ignored (otherwise, there's no traceback).

    >>> run(argv=["nosetests", "--with-todo", misc_test],
    ...     plugins=[TodoPlugin(), Skip(), Deprecated()])
    ... # doctest: +REPORT_NDIFF
    T.SSDD
    ======================================================================
    TODO: errorclass_tests.test_todo
    ----------------------------------------------------------------------
    Traceback (most recent call last):
    ...
    Todo: fix me
    <BLANKLINE>
    ----------------------------------------------------------------------
    Ran 6 tests in ...s
    <BLANKLINE>
    FAILED (DEPRECATED=2, SKIP=2, TODO=1)

>>> sys.path.remove(support)
