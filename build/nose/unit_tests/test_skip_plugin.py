import unittest
from nose.config import Config
from nose.plugins.skip import Skip, SkipTest
from nose.result import TextTestResult
from StringIO import StringIO
from nose.result import _TextTestResult
from optparse import OptionParser
try:
    # 2.7+
    from unittest.runner import _WritelnDecorator
except ImportError:
    from unittest import _WritelnDecorator


class TestSkipPlugin(unittest.TestCase):

    def test_api_present(self):
        sk = Skip()
        sk.addOptions
        sk.configure
        sk.prepareTestResult

    def test_prepare_patches_result(self):
        stream = _WritelnDecorator(StringIO())
        res = _TextTestResult(stream, 0, 1)
        sk = Skip()
        sk.prepareTestResult(res)
        res._orig_addError
        res._orig_printErrors
        res._orig_wasSuccessful
        res.skipped
        self.assertEqual(res.errorClasses,
                         {SkipTest: (res.skipped, 'SKIP', False)})

        # result w/out print works too
        res = unittest.TestResult()
        sk = Skip()
        sk.prepareTestResult(res)
        res._orig_addError
        res.skipped
        self.assertEqual(res.errorClasses,
                         {SkipTest: (res.skipped, 'SKIP', False)})

    def test_patched_result_handles_skip(self):
        res = unittest.TestResult()
        sk = Skip()
        sk.prepareTestResult(res)

        class TC(unittest.TestCase):
            def test(self):
                raise SkipTest('skip me')

        test = TC('test')
        test(res)
        assert not res.errors, "Skip was not caught: %s" % res.errors
        assert res.skipped
        assert res.skipped[0][0] is test

    def test_patches_only_when_needed(self):
        class NoPatch(unittest.TestResult):
            def __init__(self):
                self.errorClasses = {}

        res = NoPatch()
        sk = Skip()
        sk.prepareTestResult(res)
        assert not hasattr(res, '_orig_addError'), \
               "Skip patched a result class it didn't need to patch"


    def test_skip_output(self):
        class TC(unittest.TestCase):
            def test(self):
                raise SkipTest('skip me')

        stream = _WritelnDecorator(StringIO())
        res = _TextTestResult(stream, 0, 1)
        sk = Skip()
        sk.prepareTestResult(res)

        test = TC('test')
        test(res)
        assert not res.errors, "Skip was not caught: %s" % res.errors
        assert res.skipped

        res.printErrors()
        out = stream.getvalue()
        print out
        assert out
        assert out.strip() == "S"
        assert res.wasSuccessful()

    def test_skip_output_verbose(self):

        class TC(unittest.TestCase):
            def test(self):
                raise SkipTest('skip me too')

        stream = _WritelnDecorator(StringIO())
        res = _TextTestResult(stream, 0, verbosity=2)
        sk = Skip()
        sk.prepareTestResult(res)
        test = TC('test')
        test(res)
        assert not res.errors, "Skip was not caught: %s" % res.errors
        assert res.skipped

        res.printErrors()
        out = stream.getvalue()
        print out
        assert out

        assert ' ... SKIP' in out
        assert 'skip me too' in out

    def test_enabled_by_default(self):
        sk = Skip()
        assert sk.enabled, "Skip was not enabled by default"

    def test_can_be_disabled(self):
        parser = OptionParser()
        sk = Skip()
        sk.addOptions(parser)
        options, args = parser.parse_args(['--no-skip'])
        sk.configure(options, Config())
        assert not sk.enabled, "Skip was not disabled by noSkip option"
        

if __name__ == '__main__':
    unittest.main()
