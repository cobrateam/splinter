import unittest

class Tests(unittest.TestCase):

    def setUp(self):
        self.value = 1

    def test_value(self):
        self.assertEqual(self.value, 1)
