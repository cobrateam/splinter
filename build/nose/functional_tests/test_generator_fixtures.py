from nose.tools import eq_
called = []

def outer_setup():
    called.append('outer_setup')

def outer_teardown():
    called.append('outer_teardown')

def inner_setup():
    called.append('inner_setup')

def inner_teardown():
    called.append('inner_teardown')

def test_gen():
    called[:] = []
    for i in range(0, 5):
        yield check, i
        
def check(i):
    expect = ['outer_setup']
    for x in range(0, i):
        expect.append('inner_setup')
        expect.append('inner_teardown')
    expect.append('inner_setup')
    eq_(called, expect)

    
test_gen.setup = outer_setup
test_gen.teardown = outer_teardown
check.setup = inner_setup
check.teardown = inner_teardown


class TestClass(object):
    def setup(self):
        print "setup called in", self
        self.called = ['setup']

    def teardown(self):
        print "teardown called in", self
        eq_(self.called, ['setup'])
        self.called.append('teardown')

    def test(self):
        print "test called in", self
        for i in range(0, 5):
            yield self.check, i

    def check(self, i):
        print "check called in", self
        expect = ['setup']
        #for x in range(0, i):
        #    expect.append('setup')
        #    expect.append('teardown')
        #expect.append('setup')
        eq_(self.called, expect)
