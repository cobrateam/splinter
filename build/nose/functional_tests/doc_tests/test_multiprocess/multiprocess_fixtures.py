from nose.plugins.skip import SkipTest
from nose.plugins.multiprocess import MultiProcess

_multiprocess_can_split_ = True

def setup_module():
    try:
        import multiprocessing
        if 'active' in MultiProcess.status:
            raise SkipTest("Multiprocess plugin is active. Skipping tests of "
                           "plugin itself.")
    except ImportError:
        raise SkipTest("multiprocessing module not available")



