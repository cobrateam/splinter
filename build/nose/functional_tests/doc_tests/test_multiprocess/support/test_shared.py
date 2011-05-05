import os
import sys

here = os.path.dirname(__file__)
flag = os.path.join(here, 'shared_flag')

_multiprocess_shared_ = 1

def _log(val):
    ff = open(flag, 'a+')
    ff.write(val)
    ff.write("\n")
    ff.close()


def _clear():
    if os.path.isfile(flag):
        os.unlink(flag)

        
def logged():
    return [line for line in open(flag, 'r')]


def setup():
    print >> sys.stderr, "setup called"
    _log('setup')


def teardown():
    print >> sys.stderr, "teardown called"
    _clear()

    
def test_a():
    assert len(logged()) == 1, "len(%s) !=1" % called


def test_b():
    assert len(logged()) == 1, "len(%s) !=1" % called


class TestMe:
    def setup_class(cls):
        cls._setup = True
    setup_class = classmethod(setup_class)

    def test_one(self):
        assert self._setup, "Class was not set up"
