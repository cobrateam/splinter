import imp
import sys
from nose.config import Config
from nose import proxy
from nose.plugins.manager import NoPlugins
from nose.util import odict


def mod(name):
    m = imp.new_module(name)
    sys.modules[name] = m
    return m
    
class ResultProxyFactory:
    def __call__(self, result, test):
        return ResultProxy(result, test)


class ResultProxy(proxy.ResultProxy):
    called = []
    def __init__(self, result, test):
        self.result = result
        self.test = test
    def afterTest(self, test):
        self.assertMyTest(test)
        self.called.append(('afterTest', test))
    def beforeTest(self, test):
        self.assertMyTest(test)
        self.called.append(('beforeTest', test))
    def startTest(self, test):
        print "proxy startTest"
        self.assertMyTest(test)
        self.called.append(('startTest', test))
    def stopTest(self, test):
        print "proxy stopTest"
        self.assertMyTest(test)
        self.called.append(('stopTest', test))
    def addDeprecated(self, test, err):
        print "proxy addDeprecated"
        self.assertMyTest(test)
        self.called.append(('addDeprecated', test, err))
    def addError(self, test, err):
        print "proxy addError"
        self.assertMyTest(test)
        self.called.append(('addError', test, err))
    def addFailure(self, test, err):
        print "proxy addFailure"
        self.assertMyTest(test)
        self.called.append(('addFailure', test, err))
    def addSkip(self, test, err):
        print "proxy addSkip"
        self.assertMyTest(test)
        self.called.append(('addSkip', test, err))
    def addSuccess(self, test):
        self.assertMyTest(test)
        self.called.append(('addSuccess', test))
    

class RecordingPluginManager(object):

    def __init__(self):
        self.reset()

    def __getattr__(self, call):
        return RecordingPluginProxy(self, call)

    def null_call(self, call, *arg, **kw):
        return getattr(self._nullPluginManager, call)(*arg, **kw)

    def reset(self):
        self._nullPluginManager = NoPlugins()
        self.called = odict()

    def calls(self):
        return self.called.keys()


class RecordingPluginProxy(object):

    def __init__(self, manager, call):
        self.man = manager
        self.call = call

    def __call__(self, *arg, **kw):
        self.man.called.setdefault(self.call, []).append((arg, kw))
        return self.man.null_call(self.call, *arg, **kw)


class Bucket(object):
    def __init__(self, **kw):
        self.__dict__['d'] = {}
        self.__dict__['d'].update(kw)
        
    def __getattr__(self, attr):
        if not self.__dict__.has_key('d'):
            return None
        return self.__dict__['d'].get(attr)

    def __setattr__(self, attr, val):        
        self.d[attr] = val


class MockOptParser(object):
    def __init__(self):
        self.opts = []
    def add_option(self, *args, **kw):
        self.opts.append((args, kw))
