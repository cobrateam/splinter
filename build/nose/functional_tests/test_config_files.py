import logging
import os
import unittest
from nose.config import Config

support = os.path.join(os.path.dirname(__file__), 'support')

class TestConfigurationFromFile(unittest.TestCase):
    def setUp(self):
        self.cfg_file = os.path.join(support, 'test.cfg')
        # install mock root logger so that these tests don't stomp on
        # the real logging config of the test runner
        class MockLogger(logging.Logger):
            root = logging.RootLogger(logging.WARNING)
            manager = logging.Manager(root)
        
        self.real_logger = logging.Logger
        self.real_root = logging.root
        logging.Logger = MockLogger
        logging.root = MockLogger.root

    def tearDown(self):
        # reset real root logger
        logging.Logger = self.real_logger
        logging.root = self.real_root
        
    def test_load_config_file(self):
        c = Config(files=self.cfg_file)
        c.configure(['test_load_config_file'])
        self.assertEqual(c.verbosity, 10)

    def test_config_file_set_by_arg(self):
        c = Config()
        c.configure(['test_config_file_set_by_arg',
                     '-c', self.cfg_file, '-v'])
        # 10 from file, 1 more from cmd line
        self.assertEqual(c.verbosity, 11)


if __name__ == '__main__':
    unittest.main()
