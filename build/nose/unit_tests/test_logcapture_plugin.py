import sys
from optparse import OptionParser
from nose.pyversion import UNICODE_STRINGS
from nose.config import Config
from nose.plugins.logcapture import LogCapture
from nose.tools import eq_
import logging
from logging import StreamHandler
import unittest

if sys.version_info >= (2, 7):
    py27 = True
else:
    py27 = False

class TestLogCapturePlugin(object):

    def test_enabled_by_default(self):
        c = LogCapture()
        assert c.enabled

    def test_default_options(self):
        c = LogCapture()
        parser = OptionParser()
        c.addOptions(parser)

        options, args = parser.parse_args(['default_options'])
        c.configure(options, Config())
        assert c.enabled
        eq_(LogCapture.logformat, c.logformat)
        eq_(LogCapture.clear, c.clear)
        eq_(LogCapture.filters, c.filters)

    def test_disable_option(self):
        parser = OptionParser()
        c = LogCapture()
        c.addOptions(parser)
        options, args = parser.parse_args(['test_can_be_disabled_long',
                                           '--nologcapture'])
        c.configure(options, Config())
        assert not c.enabled

        env = {'NOSE_NOLOGCAPTURE': 1}
        c = LogCapture()
        parser = OptionParser()
        c.addOptions(parser, env)
        options, args = parser.parse_args(['test_can_be_disabled'])
        c.configure(options, Config())
        assert not c.enabled

    def test_logging_format_option(self):
        env = {'NOSE_LOGFORMAT': '++%(message)s++'}
        c = LogCapture()
        parser = OptionParser()
        c.addOptions(parser, env)
        options, args = parser.parse_args(['logging_format'])
        c.configure(options, Config())
        eq_('++%(message)s++', c.logformat)

    def test_logging_datefmt_option(self):
        env = {'NOSE_LOGDATEFMT': '%H:%M:%S'}
        c = LogCapture()
        parser = OptionParser()
        c.addOptions(parser, env)
        options, args = parser.parse_args(['logging_datefmt'])
        c.configure(options, Config())
        eq_('%H:%M:%S', c.logdatefmt)

    def test_captures_logging(self):
        c = LogCapture()
        parser = OptionParser()
        c.addOptions(parser, {})
        options, args = parser.parse_args([])
        c.configure(options, Config())
        c.start()
        log = logging.getLogger("foobar.something")
        log.debug("Hello")
        c.end()
        eq_(1, len(c.handler.buffer))
        eq_("Hello", c.handler.buffer[0].msg)

    def test_clears_all_existing_log_handlers(self):
        c = LogCapture()
        parser = OptionParser()
        c.addOptions(parser, {})
        options, args = parser.parse_args(['--logging-clear-handlers'])
        c.configure(options, Config())
        eq_(c.clear, True)

        def mktest():
            class TC(unittest.TestCase):
                def runTest(self):
                    pass
            test = TC()
            return test

        logging.getLogger().addHandler(StreamHandler(sys.stdout))
        log = logging.getLogger("dummy")
        log.addHandler(StreamHandler(sys.stdout))

        c.start()
        c.beforeTest(mktest())
        c.end()


        if py27:
            expect = ["<class 'nose.plugins.logcapture.MyMemoryHandler'>"]
        else:
            expect = ['nose.plugins.logcapture.MyMemoryHandler']
        eq_([str(c.__class__) for c in logging.getLogger().handlers],
            expect)
        eq_([str(c.__class__) for c in logging.getLogger("dummy").handlers],
            [])

    def test_custom_formatter(self):
        c = LogCapture()
        c.logformat = '++%(message)s++'
        c.start()
        log = logging.getLogger("foobar.something")
        log.debug("Hello")
        c.end()
        records = c.formatLogRecords()
        eq_(1, len(records))
        eq_("++Hello++", records[0])

    def test_logging_filter(self):
        env = {'NOSE_LOGFILTER': 'foo,bar'}
        c = LogCapture()
        parser = OptionParser()
        c.addOptions(parser, env)
        options, args = parser.parse_args(['foo'])
        print options, args
        c.configure(options, Config())
        c.start()
        for name in ['foobar.something', 'foo', 'foo.x', 'abara', 'bar.quux']:
            log = logging.getLogger(name)
            log.info("Hello %s" % name)
        c.end()
        records = c.formatLogRecords()
        eq_(3, len(records))
        assert records[0].startswith('foo:'), records[0]
        assert records[1].startswith('foo.x:'), records[1]
        assert records[2].startswith('bar.quux:'), records[2]
        
    def test_logging_filter_exclude(self):
        env = {'NOSE_LOGFILTER': '-foo,-bar'}
        c = LogCapture()
        parser = OptionParser()
        c.addOptions(parser, env)
        options, args = parser.parse_args(['foo'])
        print options, args
        c.configure(options, Config())
        c.start()
        for name in ['foobar.something', 'foo', 'foo.x', 'abara', 'bar.quux']:
            log = logging.getLogger(name)
            log.info("Hello %s" % name)
        c.end()
        records = c.formatLogRecords()
        eq_(2, len(records))
        assert records[0].startswith('foobar.something:'), records[0]
        assert records[1].startswith('abara:'), records[1]
        
    def test_logging_filter_exclude_and_include(self):
        env = {'NOSE_LOGFILTER': 'foo,-foo.bar'}
        c = LogCapture()
        parser = OptionParser()
        c.addOptions(parser, env)
        options, args = parser.parse_args(['foo'])
        print options, args
        c.configure(options, Config())
        c.start()
        for name in ['foo.yes', 'foo.bar', 'foo.bar.no', 'blah']:
            log = logging.getLogger(name)
            log.info("Hello %s" % name)
        c.end()
        records = c.formatLogRecords()
        eq_(1, len(records))
        assert records[0].startswith('foo.yes:'), records[0]

    def test_unicode_messages_handled(self):
        msg = u'Ivan Krsti\u0107'
        c = LogCapture()
        parser = OptionParser()
        c.addOptions(parser, {})
        options, args = parser.parse_args([])
        c.configure(options, Config())
        c.start()
        log = logging.getLogger("foobar.something")
        log.debug(msg)
        log.debug("ordinary string log")
        c.end()

        class Dummy:
            pass
        test = Dummy() 
        try:
            raise Exception(msg)
        except:
            err = sys.exc_info()
        (ec, ev, tb) = c.formatError(test, err)
        print ev
        if UNICODE_STRINGS:
            assert msg in ev
        else:
            assert msg.encode('utf-8') in ev
