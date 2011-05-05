import example
import unittest

class TestExampleFunction_TestCase(unittest.TestCase):
    def test_times_two(self):
        self.assertEqual(example.times_two(2), 4)


class TestExampleFunction:
    def test_times_two(self):
        assert example.times_two(2) == 4


def test_times_two():
    assert example.times_two(2) == 4
