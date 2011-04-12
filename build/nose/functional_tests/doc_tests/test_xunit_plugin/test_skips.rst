XUnit output supports skips
---------------------------

>>> import os
>>> from nose.plugins.xunit import Xunit
>>> from nose.plugins.skip import SkipTest, Skip
>>> support = os.path.join(os.path.dirname(__file__), 'support')
>>> outfile = os.path.join(support, 'nosetests.xml')
>>> from nose.plugins.plugintest import run_buffered as run
>>> argv = [__file__, '-v', '--with-xunit', support,
...         '--xunit-file=%s' % outfile]
>>> run(argv=argv, plugins=[Xunit(), Skip()]) # doctest: +ELLIPSIS
test_skip.test_ok ... ok
test_skip.test_err ... ERROR
test_skip.test_fail ... FAIL
test_skip.test_skip ... SKIP: not me
<BLANKLINE>
======================================================================
ERROR: test_skip.test_err
----------------------------------------------------------------------
Traceback (most recent call last):
...
Exception: oh no
<BLANKLINE>
======================================================================
FAIL: test_skip.test_fail
----------------------------------------------------------------------
Traceback (most recent call last):
...
AssertionError: bye
<BLANKLINE>
----------------------------------------------------------------------
XML: ...nosetests.xml
----------------------------------------------------------------------
Ran 4 tests in ...s
<BLANKLINE>
FAILED (SKIP=1, errors=1, failures=1)

>>> open(outfile, 'r').read() # doctest: +ELLIPSIS
'<?xml version="1.0" encoding="UTF-8"?><testsuite name="nosetests" tests="4" errors="1" failures="1" skip="1"><testcase classname="test_skip" name="test_ok" time="..." /><testcase classname="test_skip" name="test_err" time="..."><error type="...Exception" message="oh no">...</error></testcase><testcase classname="test_skip" name="test_fail" time="..."><failure type="...AssertionError" message="bye">...</failure></testcase><testcase classname="test_skip" name="test_skip" time="..."><skipped type="...SkipTest" message="not me">...</skipped></testcase></testsuite>'
