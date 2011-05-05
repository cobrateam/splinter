import mymodule
import testlib

class MyFunction(testlib.Base):

    def test_tuple_groups(self):
        self.assertEqual(mymodule.my_function(1, 2, 3), (1, (2, 3)))
