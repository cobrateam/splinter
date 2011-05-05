import os
import sys
import unittest
from cStringIO import StringIO
from nose.config import Config
from nose.core import TestProgram
from nose.plugins.manager import PluginManager


support = os.path.join(os.path.dirname(__file__), 'support')

class TestResultSummary(unittest.TestCase):

    def test_with_todo_plugin(self):
        pkpath = os.path.join(support, 'todo')
        sys.path.insert(0, pkpath)
        from todoplug import TodoPlugin

        stream = StringIO()
        config = Config(stream=stream,
                        plugins=PluginManager([TodoPlugin()]))
        
        TestProgram(argv=['t', '--with-todo', pkpath],
                    config=config, exit=False)
        out = stream.getvalue()
        print out
        self.assert_('FAILED (TODO=1)' in out)


if __name__ == '__main__':
    unittest.main()
        
