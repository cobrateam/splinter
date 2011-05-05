import logging
import unittest
from nose.config import Config
#from nose.core import configure_logging
from mock import *


class TestLoggingConfig(unittest.TestCase):

    def setUp(self):
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
        
    def test_isolation(self):
        """root logger settings ignored"""

        root = logging.getLogger('')
        nose = logging.getLogger('nose')

        config = Config()
        config.configureLogging()
        
        root.setLevel(logging.DEBUG)
        self.assertEqual(nose.level, logging.WARN)
    
if __name__ == '__main__':
    unittest.main()
