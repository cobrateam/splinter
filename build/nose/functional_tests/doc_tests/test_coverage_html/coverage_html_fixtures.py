import sys
import os
from nose.plugins.skip import SkipTest
from nose.plugins.cover import Coverage
from nose.plugins.plugintest import munge_nose_output_for_doctest

_multiprocess_can_split_ = True

def setup_module():
    try:
        import coverage
        if 'active' in Coverage.status:
            raise SkipTest("Coverage plugin is active. Skipping tests of "
                           "plugin itself.")
    except ImportError:
        raise SkipTest("coverage module not available")
