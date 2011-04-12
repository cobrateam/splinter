from errorclass_failure_plugin import Todo
from nose import SkipTest, DeprecatedTest

def test_todo():
    raise Todo('fix me')

def test_2():
    pass

def test_3():
    raise SkipTest('skipety-skip')

def test_4():
    raise SkipTest()

def test_5():
    raise DeprecatedTest('spam\neggs\n\nspam')

def test_6():
    raise DeprecatedTest('spam')
