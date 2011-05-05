import testlib
from mypackage import math


class TestBasicMath(testlib.Base):

    def test_add(self):
        self.assertEqual(math.add(1, 2), 3)

    def test_sub(self):
        self.assertEqual(math.sub(3, 1), 2)


class TestHelperClass:
    def __init__(self):
        raise Exception(
            "This test helper class should not be collected")
