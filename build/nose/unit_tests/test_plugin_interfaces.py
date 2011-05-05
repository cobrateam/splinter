import unittest
from nose.plugins.base import IPluginInterface

class TestPluginInterfaces(unittest.TestCase):

    def test_api_methods_present(self):

        from nose.loader import TestLoader
        from nose.selector import Selector

        
        exclude = [ 'loadTestsFromGenerator',
                    'loadTestsFromGeneratorMethod'
                    ]
        
        selfuncs = [ f for f in dir(Selector)
                     if f.startswith('want') ]
        loadfuncs = [ f for f in dir(TestLoader)
                      if f.startswith('load') and not f in exclude ]
        
        others = ['addDeprecated', 'addError', 'addFailure',
                  'addSkip', 'addSuccess', 'startTest', 'stopTest',
                  'prepareTest', 'begin', 'report'
                  ] 

        expect = selfuncs + loadfuncs + others
        
        pd = dir(IPluginInterface)
        
        for f in expect:
            assert f in pd, "No %s in IPluginInterface" % f
            assert getattr(IPluginInterface, f).__doc__, \
                "No docs for %f in IPluginInterface" % f
            
    def test_no_instantiate(self):
        try:
            p = IPluginInterface()
        except TypeError:
            pass
        else:
            assert False, \
                "Should not be able to instantiate IPluginInterface"
            
if __name__ == '__main__':
    unittest.main()
