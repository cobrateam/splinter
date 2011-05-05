Naming a non-existent test using the colon syntax (foo.py:my_test)
with plugin doctests enabled used to cause a failure with a ValueError
from module doctest, losing the original failure (failure to find the
test).

    >>> import os
    >>> from nose.plugins.plugintest import run_buffered as run
    >>> from nose.plugins.doctests import Doctest

    >>> support = os.path.join(os.path.dirname(__file__), 'support')
    >>> test_name = os.path.join(support, 'some_test.py') + ':nonexistent'
    >>> run(argv=['nosetests', '--with-doctest', test_name],
    ...     plugins=[Doctest()])
    E
    ======================================================================
    ERROR: Failure: ValueError (No such test nonexistent)
    ----------------------------------------------------------------------
    Traceback (most recent call last):
    ...
    ValueError: No such test nonexistent
    <BLANKLINE>
    ----------------------------------------------------------------------
    Ran 1 test in ...s
    <BLANKLINE>
    FAILED (errors=1)
