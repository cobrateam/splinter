import re
import os
import tempfile
import unittest
import warnings
import pickle
import sys

import nose.config
from nose.plugins.manager import DefaultPluginManager
from nose.plugins.skip import SkipTest
from nose.plugins.prof import Profile


class TestNoseConfig(unittest.TestCase):

    def test_defaults(self):
        c = nose.config.Config()
        assert c.addPaths == True
        # FIXME etc

    def test_reset(self):
        c = nose.config.Config()
        c.include = 'include'
        assert c.include == 'include'
        c.reset()
        assert c.include is None

    def test_update(self):
        c = nose.config.Config()
        c.update({'exclude':'x'})
        assert c.exclude == 'x'

    def test_multiple_include(self):
        c = nose.config.Config()
        c.configure(['program', '--include=a', '--include=b'])
        self.assertEqual(len(c.include), 2)
        a, b = c.include
        assert a.match('a')
        assert not a.match('b')
        assert b.match('b')
        assert not b.match('a')

    def test_single_include(self):
        c = nose.config.Config()
        c.configure(['program', '--include=b'])
        self.assertEqual(len(c.include), 1)
        b = c.include[0]
        assert b.match('b')
        assert not b.match('a')

    def test_plugins(self):
        c = nose.config.Config()
        assert c.plugins
        c.plugins.begin()

    def test_testnames(self):
        c = nose.config.Config()
        c.configure(['program', 'foo', 'bar', 'baz.buz.biz'])
        self.assertEqual(c.testNames, ['foo', 'bar', 'baz.buz.biz'])

        c = nose.config.Config(testNames=['foo'])
        c.configure([])
        self.assertEqual(c.testNames, ['foo'])

    def test_where(self):
        # we don't need to see our own warnings
        warnings.filterwarnings(action='ignore',
                                category=DeprecationWarning,
                                module='nose.config')

        here = os.path.dirname(__file__)
        support = os.path.join(here, 'support')
        foo = os.path.abspath(os.path.join(support, 'foo'))
        c = nose.config.Config()
        c.configure(['program', '-w', foo, '-w', 'bar'])
        self.assertEqual(c.workingDir, foo)
        self.assertEqual(c.testNames, ['bar'])

    def test_progname_looks_like_option(self):
        # issue #184
        c = nose.config.Config()
        # the -v here is the program name, not an option
        # this matters eg. with python -c "import nose; nose.main()"
        c.configure(['-v', 'mytests'])
        self.assertEqual(c.verbosity, 1)

    def test_pickle_empty(self):
        c = nose.config.Config()
        cp = pickle.dumps(c)
        cc = pickle.loads(cp)

    def test_pickle_configured(self):
        if 'java' in sys.version.lower():
            raise SkipTest("jython has no profiler plugin")
        c = nose.config.Config(plugins=DefaultPluginManager())
        config_args = ['--with-doctest', '--with-coverage', 
                     '--with-id', '--attr=A', '--collect', '--all',
                     '--with-isolation', '-d', '--with-xunit', '--processes=2',
                     '--pdb']
        if Profile.available():
            config_args.append('--with-profile')
        c.configure(config_args)
        cp = pickle.dumps(c)
        cc = pickle.loads(cp)
        assert cc.plugins._plugins


if __name__ == '__main__':
    unittest.main()
