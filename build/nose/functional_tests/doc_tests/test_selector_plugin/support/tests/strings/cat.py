import testlib
from mypackage import strings

class StringsCat(testlib.Base):

    def test_cat(self):
        self.assertEqual(strings.cat('one', 'two'), 'onetwo')


def test_helper_function():
    raise Exception(
        "This test helper function should not be collected")
