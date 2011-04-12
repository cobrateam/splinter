# -*- encoding: utf-8 -*-
from nose.plugins.skip import SkipTest
import sys


def setup():
    if 'java' in sys.version.lower():
        raise SkipTest("StringIO() in jython can't handle unicode")


def test_unicode():
    print u'b\u00f6y'
