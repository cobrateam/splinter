import os
import re
import sys
import tempfile
import unittest

from nose.plugins import PluginTester
from nose.plugins.builtin import Doctest
from nose.plugins.builtin import TestId
from cPickle import dump, load

support = os.path.join(os.path.dirname(__file__), 'support')
idfile = tempfile.mktemp()
test_part = re.compile(r'(#\d+)? +([^(]+)')

def teardown():
     try:
         os.remove(idfile)
     except OSError:
         pass

class TestDiscoveryMode(PluginTester, unittest.TestCase):
    activate = '--with-id'
    plugins = [TestId()]
    args = ['-v', '--id-file=%s' % idfile]
    suitepath = os.path.join(support, 'idp')

    def test_ids_added_to_output(self):
        #print '>' * 70
        #print str(self.output)
        #print '<' * 70

        for line in self.output:
            if line.startswith('='):
                break
            if not line.strip():
                continue
            if 'test_gen' in line and not '(0,)' in line:
                assert not line.startswith('#'), \
                       "Generated test line '%s' should not have id" % line
            else:
                assert line.startswith('#'), \
                       "Test line '%s' missing id" % line.strip()
            
    # test that id file is written
    def test_id_file_contains_ids_seen(self):
        assert os.path.exists(idfile)
        fh = open(idfile, 'rb')
        ids = load(fh)['ids']
        fh.close()
        assert ids
        assert ids.keys()
        self.assertEqual(map(int, ids.keys()), ids.keys())
        assert ids.values()


class TestLoadNamesMode(PluginTester, unittest.TestCase):
    """NOTE that this test passing requires the previous test case to
    be run! (Otherwise the ids file will not exist)
    """
    activate = '--with-id'
    plugins = [TestId()]
    # Not a typo: # is optional before ids
    args = ['-v', '--id-file=%s' % idfile, '2', '#5']
    suitepath = None

    def makeSuite(self):
        return None

    def test_load_ids(self):
        #print '#' * 70
        #print str(self.output)
        #print '#' * 70

        for line in self.output:
            if line.startswith('#'):
                assert line.startswith('#2 ') or line.startswith('#5 '), \
                       "Unexpected test line '%s'" % line
        assert os.path.exists(idfile)
        fh = open(idfile, 'rb')
        ids = load(fh)
        fh.close()
        assert ids
        assert ids.keys()
        ids = ids['ids']
        self.assertEqual(filter(lambda i: int(i), ids.keys()), ids.keys())
        assert len(ids.keys()) > 2


class TestLoadNamesMode_2(PluginTester, unittest.TestCase):
    """NOTE that this test passing requires the previous test case to
    be run! (Otherwise the ids file will not exist)

    Tests that generators still only have id on one line
    """
    activate = '--with-id'
    plugins = [TestId()]
    args = ['-v', '--id-file=%s' % idfile, '9']
    suitepath = None

    def makeSuite(self):
        return None

    def test_load_ids(self):
        #print '%' * 70
        #print str(self.output)
        #print '%' * 70

        count = 0
        for line in self.output:
            if line.startswith('#'):
                count += 1
        self.assertEqual(count, 1)
        teardown()


class TestWithDoctest_1(PluginTester, unittest.TestCase):
    activate = '--with-id'
    plugins = [Doctest(), TestId()]
    args = ['-v', '--id-file=%s' % idfile, '--with-doctest']
    suitepath = os.path.join(support, 'idp')

    def test_doctests_get_ids(self):
        #print '>' * 70
        #print str(self.output)
        #print '>' * 70

        last = None
        for line in self.output:
            if line.startswith('='):
                break
            if not line.strip():
                continue
            # assert line startswith # or test part matches last
            m = test_part.match(line.rstrip())
            assert m
            idx, name = m.groups()
            assert idx or last is None or name == last, \
                   "Expected an id on line %s" % line.strip()
            last = name
            
        fh = open(idfile, 'rb')
        ids = load(fh)['ids']
        fh.close()
        for key, (file, mod, call) in ids.items():
            assert mod != 'doctest', \
                   "Doctest test was incorrectly identified as being part of "\
                   "the doctest module itself (#%s)" % key


class TestWithDoctest_2(PluginTester, unittest.TestCase):
    activate = '--with-id'
    plugins = [Doctest(), TestId()]
    args = ['-v', '--id-file=%s' % idfile, '--with-doctest', '#2']
    suitepath = None

    def setUp(self):
        sys.path.insert(0, os.path.join(support, 'idp'))
        super(TestWithDoctest_2, self).setUp()

    def tearDown(self):
        sys.path.remove(os.path.join(support, 'idp'))
        super(TestWithDoctest_2, self).tearDown()

    def makeSuite(self):
        return None

    def test_load_ids_doctest(self):
        print '*' * 70
        print str(self.output)
        print '*' * 70

        assert 'Doctest: exm.add_one ... FAIL' in self.output
        
        count = 0
        for line in self.output:
            if line.startswith('#'):
                count += 1
        self.assertEqual(count, 1)
        teardown()
        

class TestWithDoctestFileTests_1(PluginTester, unittest.TestCase):
    activate = '--with-id'
    plugins = [Doctest(), TestId()]
    args = ['-v', '--id-file=%s' % idfile, '--with-doctest',
            '--doctest-extension=.txt']
    suitepath = os.path.join(support, 'dtt', 'docs')

    def test_docfile_tests_get_ids(self):
        print '>' * 70
        print str(self.output)
        print '>' * 70

        last = None
        for line in self.output:
            if line.startswith('='):
                break
            # assert line startswith # or test part matches last
            if not line.strip():
                continue
            m = test_part.match(line.rstrip())
            assert m, "line %s does not match expected pattern" % line.strip()
            idx, name = m.groups()
            assert idx or last is None or name == last, \
                   "Expected an id on line %s" % line.strip()
            
            last = name
        fh = open(idfile, 'rb')
        ids = load(fh)['ids']
        fh.close()
        for key, (file, mod, call) in ids.items():
            assert mod != 'doctest', \
                   "Doctest test was incorrectly identified as being part of "\
                   "the doctest module itself (#%s)" % key    


class TestWithDoctestFileTests_2(PluginTester, unittest.TestCase):
    activate = '--with-id'
    plugins = [Doctest(), TestId()]
    args = ['-v', '--id-file=%s' % idfile, '--with-doctest',
            '--doctest-extension=.txt', '2']
    suitepath = None

    def setUp(self):
        sys.path.insert(0, os.path.join(support, 'dtt', 'docs'))
        super(TestWithDoctestFileTests_2, self).setUp()

    def tearDown(self):
        sys.path.remove(os.path.join(support, 'dtt', 'docs'))
        super(TestWithDoctestFileTests_2, self).tearDown()

    def makeSuite(self):
        return None

    def test_load_from_name_id_docfile_test(self):
        print '*' * 70
        print str(self.output)
        print '*' * 70

        assert 'Doctest: errdoc.txt ... FAIL' in self.output
        
        count = 0
        for line in self.output:
            if line.startswith('#'):
                count += 1
        assert count == 1
        teardown()
        
        
if __name__ == '__main__':
    import logging
    logging.basicConfig()
    l = logging.getLogger('nose.plugins.testid')
    l.setLevel(logging.DEBUG)
    
    try:
        unittest.main()
    finally:
        teardown()
    
