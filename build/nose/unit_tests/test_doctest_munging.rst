doctest output normalization for plugin testing support
=======================================================

nose.plugins.plugintest.run() is used for testing nose plugins in
doctests, so it needs to normalise nose output to remove information
that is not of interest to most plugin tests.

We strip stack trace from formatted exceptions, using a regexp copied
from ``doctest.py``.  That regexp always matches to the end of a
string, so we split on blank lines before running the regexp on each
resulting block.

    >>> from nose.plugins.plugintest import blankline_separated_blocks
    >>> list(blankline_separated_blocks("spam\neggs\n\nfoo\nbar\n\n"))
    ['spam\neggs\n\n', 'foo\nbar\n\n']
    >>> list(blankline_separated_blocks("spam\neggs\n\nfoo\nbar\n"))
    ['spam\neggs\n\n', 'foo\nbar\n']
    >>> list(blankline_separated_blocks("spam\neggs\n\nfoo\nbar"))
    ['spam\neggs\n\n', 'foo\nbar']
    >>> list(blankline_separated_blocks(""))
    []
    >>> list(blankline_separated_blocks("spam"))
    ['spam']

``remove_stack_traces`` removes the stack traces, replacing them with
an ellipsis.  Note the first line here is chosen not to be "Traceback
(most recent...", since doctest would interpret that as meaning that
the example should raise an exception!

    >>> from nose.plugins.plugintest import remove_stack_traces
    >>> print remove_stack_traces("""\
    ... Ceci n'est pas une traceback.
    ... Traceback (most recent call last):
    ...   File "/some/dir/foomodule.py", line 15, in runTest
    ...   File "/some/dir/spam.py", line 293, in who_knows_what
    ... AssertionError: something bad happened
    ... """)
    Ceci n'est pas une traceback.
    Traceback (most recent call last):
    ...
    AssertionError: something bad happened
    <BLANKLINE>

Multiple tracebacks in an example are all replaced, as long as they're
separated by blank lines.

    >>> print remove_stack_traces("""\
    ... Ceci n'est pas une traceback.
    ... Traceback (most recent call last):
    ...   File spam
    ... AttributeError: eggs
    ...
    ... Traceback (most recent call last):
    ...   File eggs
    ... AttributeError: spam
    ... """)
    Ceci n'est pas une traceback.
    Traceback (most recent call last):
    ...
    AttributeError: eggs
    <BLANKLINE>
    Traceback (most recent call last):
    ...
    AttributeError: spam
    <BLANKLINE>


Putting it together, ``munge_nose_output_for_doctest()`` removes stack
traces, removes test timings from "Ran n test(s)" output, and strips
trailing blank lines.

    >>> from nose.plugins.plugintest import munge_nose_output_for_doctest
    >>> print munge_nose_output_for_doctest("""\
    ... runTest (foomodule.PassingTest) ... ok
    ... runTest (foomodule.FailingTest) ... FAIL
    ...
    ... ======================================================================
    ... FAIL: runTest (foomodule.FailingTest)
    ... ----------------------------------------------------------------------
    ... Traceback (most recent call last):
    ...   File "/some/dir/foomodule.py", line 15, in runTest
    ...   File "/some/dir/spam.py", line 293, in who_knows_what
    ... AssertionError: something bad happened
    ...
    ... ----------------------------------------------------------------------
    ... Ran 1 test in 0.082s
    ...
    ... FAILED (failures=1)
    ...
    ...
    ... """)
    runTest (foomodule.PassingTest) ... ok
    runTest (foomodule.FailingTest) ... FAIL
    <BLANKLINE>
    ======================================================================
    FAIL: runTest (foomodule.FailingTest)
    ----------------------------------------------------------------------
    Traceback (most recent call last):
    ...
    AssertionError: something bad happened
    <BLANKLINE>
    ----------------------------------------------------------------------
    Ran 1 test in ...s
    <BLANKLINE>
    FAILED (failures=1)
