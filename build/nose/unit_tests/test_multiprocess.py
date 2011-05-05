import pickle
import sys
import unittest

from nose import case
from nose.plugins import multiprocess
from nose.plugins.skip import SkipTest
from nose.config import Config
from nose.loader import TestLoader
try:
    # 2.7+
    from unittest.runner import _WritelnDecorator
except ImportError:
    from unittest import _WritelnDecorator


class ArgChecker:
    def __init__(self, target, args):
        self.target = target
        self.args = args
        # skip the id and queues
        pargs = args[4:]
        self.pickled = pickle.dumps(pargs)
    def start(self):
        pass
    def is_alive(self):
        return False

        
def setup(mod):
    multiprocess._import_mp()
    if not multiprocess.Process:
        raise SkipTest("multiprocessing not available")
    mod.Process = multiprocess.Process
    multiprocess.Process = ArgChecker
        

class T(unittest.TestCase):
    __test__ = False
    def runTest(self):
        pass

    
def test_mp_process_args_pickleable():
    test = case.Test(T('runTest'))
    config = Config()
    config.multiprocess_workers = 2
    config.multiprocess_timeout = 0.1
    runner = multiprocess.MultiProcessTestRunner(
        stream=_WritelnDecorator(sys.stdout),
        verbosity=2,
        loaderClass=TestLoader,
        config=config)
    runner.run(test)
        
