from nose.exc import SkipTest
from nose.tools import *
from nose.twistedtools import *
try:    
    from twisted.internet.defer import Deferred
    from twisted.internet.error import DNSLookupError
except ImportError:
    raise SkipTest('twisted not available; skipping')

_multiprocess_ = False


def teardown():
    # print "stopping reactor"
    stop_reactor()

class CustomError(Exception):
    pass

# FIXME move all dns-using tests to functional

# Should succeed unless google is down
#@deferred
def test_resolve():
    return reactor.resolve("www.google.com")
test_resolve = deferred()(test_resolve)

# Raises TypeError because the function does not return a Deferred
#@raises(TypeError)
#@deferred()
def test_raises_bad_return():
    print reactor
    reactor.resolve("nose.python-hosting.com")
test_raises_bad_return = raises(TypeError)(deferred()(test_raises_bad_return))

# Check we propagate twisted Failures as Exceptions
# (XXX this test might take some time: find something better?)
#@raises(DNSLookupError)
#@deferred()
def test_raises_twisted_error():
    return reactor.resolve("x.y.z")
test_raises_twisted_error = raises(DNSLookupError)(
    deferred()(test_raises_twisted_error))

# Check we detect Exceptions inside the callback chain
#@raises(CustomError)
#@deferred(timeout=1.0)
def test_raises_callback_error():
    d = Deferred()
    def raise_error(_):
        raise CustomError()
    def finish():
        d.callback(None)
    d.addCallback(raise_error)
    reactor.callLater(0.01, finish)
    return d
test_raises_callback_error = raises(CustomError)(
    deferred(timeout=1.0)(test_raises_callback_error))

# Check we detect Exceptions inside the test body
#@raises(CustomError)
#@deferred(timeout=1.0)
def test_raises_plain_error():
    raise CustomError
test_raises_plain_error = raises(CustomError)(
    deferred(timeout=1.0)(test_raises_plain_error))

# The deferred is triggered before the timeout: ok
#@deferred(timeout=1.0)
def test_timeout_ok():
    d = Deferred()
    def finish():
        d.callback(None)
    reactor.callLater(0.01, finish)
    return d
test_timeout_ok = deferred(timeout=1.0)(test_timeout_ok)

# The deferred is triggered after the timeout: failure
#@raises(TimeExpired)
#@deferred(timeout=0.1)
def test_timeout_expired():
    d = Deferred()
    def finish():
        d.callback(None)
    reactor.callLater(1.0, finish)
    return d
test_timeout_expired = raises(TimeExpired)(
    deferred(timeout=0.1)(test_timeout_expired))


if __name__ == '__main__':
    from nose import runmodule
    runmodule()
