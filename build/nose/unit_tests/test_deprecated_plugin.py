import unittest
from nose.config import Config
from nose.plugins.deprecated import Deprecated, DeprecatedTest
from nose.result import TextTestResult, _TextTestResult
from StringIO import StringIO
from optparse import OptionParser
try:
    # 2.7+
    from unittest.runner import _WritelnDecorator
except ImportError:
    from unittest import _WritelnDecorator


class TestDeprecatedPlugin(unittest.TestCase):

    def test_api_present(self):
        sk = Deprecated()
        sk.addOptions
        sk.configure
        sk.prepareTestResult        

    def test_prepare_patches_result(self):
        stream = _WritelnDecorator(StringIO())
        res = _TextTestResult(stream, 0, 1)
        sk = Deprecated()
        sk.prepareTestResult(res)
        res._orig_addError
        res._orig_printErrors
        res._orig_wasSuccessful
        res.deprecated
        self.assertEqual(
            res.errorClasses,
            {DeprecatedTest: (res.deprecated, 'DEPRECATED', False)})

        # result w/out print works too
        res = unittest.TestResult()
        sk = Deprecated()
        sk.prepareTestResult(res)
        res._orig_addError
        res.deprecated
        self.assertEqual(
            res.errorClasses,
            {DeprecatedTest: (res.deprecated, 'DEPRECATED', False)})

    def test_patched_result_handles_deprecated(self):
        res = unittest.TestResult()
        sk = Deprecated()
        sk.prepareTestResult(res)

        class TC(unittest.TestCase):
            def test(self):
                raise DeprecatedTest('deprecated me')

        test = TC('test')
        test(res)
        assert not res.errors, "Deprecated was not caught: %s" % res.errors
        assert res.deprecated
        assert res.deprecated[0][0] is test

    def test_patches_only_when_needed(self):
        class NoPatch(unittest.TestResult):
            def __init__(self):
                self.errorClasses = {}
                
        res = NoPatch()
        sk = Deprecated()
        sk.prepareTestResult(res)
        assert not hasattr(res, '_orig_addError'), \
               "Deprecated patched a result class it didn't need to patch"
        

    def test_deprecated_output(self):
        class TC(unittest.TestCase):
            def test(self):
                raise DeprecatedTest('deprecated me')

        stream = _WritelnDecorator(StringIO())
        res = _TextTestResult(stream, 0, 1)
        sk = Deprecated()
        sk.prepareTestResult(res)

        test = TC('test')
        test(res)
        assert not res.errors, "Deprecated was not caught: %s" % res.errors
        assert res.deprecated            

        res.printErrors()
        out = stream.getvalue()
        assert out
        assert out.strip() == "D"
        assert res.wasSuccessful()

    def test_deprecated_output_verbose(self):

        class TC(unittest.TestCase):
            def test(self):
                raise DeprecatedTest('deprecated me too')
        
        stream = _WritelnDecorator(StringIO())
        res = _TextTestResult(stream, 0, verbosity=2)
        sk = Deprecated()
        sk.prepareTestResult(res)
        test = TC('test')
        test(res)
        assert not res.errors, "Deprecated was not caught: %s" % res.errors
        assert res.deprecated            

        res.printErrors()
        out = stream.getvalue()
        print out
        assert out

        assert ' ... DEPRECATED' in out
        assert 'deprecated me too' in out

    def test_enabled_by_default(self):
        sk = Deprecated()
        assert sk.enabled, "Deprecated was not enabled by default"

    def test_can_be_disabled(self):
        parser = OptionParser()
        sk = Deprecated()
        sk.addOptions(parser)
        options, args = parser.parse_args(['--no-deprecated'])
        sk.configure(options, Config())
        assert not sk.enabled, \
               "Deprecated was not disabled by noDeprecated option"
        

if __name__ == '__main__':
    unittest.main()
