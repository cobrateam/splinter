# -*- coding: utf-8 -*-
import sys
import unittest
from optparse import OptionParser
from nose.config import Config
from nose.plugins.capture import Capture

class TestCapturePlugin(unittest.TestCase):

    def setUp(self):
        self._stdout = sys.stdout

    def tearDown(self):
        sys.stdout = self._stdout

    def test_enabled_by_default(self):
        c = Capture()
        assert c.enabled

    def test_can_be_disabled(self):
        c = Capture()
        parser = OptionParser()
        c.addOptions(parser)
        options, args = parser.parse_args(['test_can_be_disabled',
                                           '-s'])
        c.configure(options, Config())
        assert not c.enabled

        c = Capture()
        options, args = parser.parse_args(['test_can_be_disabled_long',
                                           '--nocapture'])
        c.configure(options, Config())
        assert not c.enabled

        env = {'NOSE_NOCAPTURE': 1}
        c = Capture()
        parser = OptionParser()
        c.addOptions(parser, env)
        options, args = parser.parse_args(['test_can_be_disabled'])
        c.configure(options, Config())
        assert not c.enabled

        c = Capture()
        parser = OptionParser()
        c.addOptions(parser)
        
        options, args = parser.parse_args(['test_can_be_disabled'])
        c.configure(options, Config())
        assert c.enabled
        
    def test_captures_stdout(self):
        c = Capture()
        c.start()
        print "Hello"
        c.end()
        self.assertEqual(c.buffer, "Hello\n")
        
    def test_captures_nonascii_stdout(self):
        c = Capture()
        c.start()
        print "test 日本"
        c.end()
        self.assertEqual(c.buffer, "test 日本\n")

    def test_format_error(self):
        class Dummy:
            pass
        d = Dummy()
        c = Capture()
        c.start()
        try:
            print "Oh my!"
            raise Exception("boom")
        except:
            err = sys.exc_info()
        formatted = c.formatError(d, err)
        ec, ev, tb = err
        (fec, fev, ftb) = formatted
        # print fec, fev, ftb
        
        self.assertEqual(ec, fec)
        self.assertEqual(tb, ftb)
        assert 'Oh my!' in fev, "Output not found in error message"
        assert 'Oh my!' in d.capturedOutput, "Output not attached to test"

if __name__ == '__main__':
    unittest.main()
