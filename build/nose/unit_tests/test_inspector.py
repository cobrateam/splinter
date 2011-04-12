import inspect
import sys
import textwrap
import tokenize
import traceback
import unittest

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

from nose.inspector import inspect_traceback, Expander, tbsource

class TestExpander(unittest.TestCase):

    def test_simple_inspect_frame(self):
        src = StringIO('a > 2')
        lc = { 'a': 2}
        gb = {}
        exp = Expander(lc, gb)
        
        for tok in tokenize.generate_tokens(src.readline):
            exp(*tok)
        # print "'%s'" % exp.expanded_source
        self.assertEqual(exp.expanded_source.strip(), '2 > 2')

    def test_inspect_traceback_continued(self):
        a = 6
        out = ''
        try:
            assert a < 1, \
                "This is a multline expression"
        except AssertionError:
            et, ev, tb = sys.exc_info()
            out = inspect_traceback(tb)
            # print "'%s'" % out.strip()
            self.assertEqual(out.strip(),
                             '>>  assert 6 < 1, \\\n        '
                             '"This is a multline expression"')

    def test_get_tb_source_simple(self):
        # no func frame
        try:
            assert False
        except AssertionError:
            et, ev, tb = sys.exc_info()
            lines, lineno = tbsource(tb, 1)
            self.assertEqual(''.join(lines).strip(), 'assert False')
            self.assertEqual(lineno, 0)

    def test_get_tb_source_func(self):        
        # func frame
        def check_even(n):
            print n
            assert n % 2 == 0
        try:
            check_even(1)
        except AssertionError:
            et, ev, tb = sys.exc_info()
            lines, lineno = tbsource(tb)
            out = textwrap.dedent(''.join(lines))
            if sys.version_info < (3,):
                first_line = '    print n\n'
            else:
                first_line = '    print(n)\n'
            self.assertEqual(out,
                             first_line +
                             '    assert n % 2 == 0\n'
                             'try:\n'
                             '    check_even(1)\n'
                             'except AssertionError:\n'
                             '    et, ev, tb = sys.exc_info()\n'
                             )
            self.assertEqual(lineno, 3)
            
        # FIXME 2 func frames
            
    def test_pick_tb_lines(self):
        try:
            val = "fred"
            def defred(n):
                return n.replace('fred','')
            assert defred(val) == 'barney', "Fred - fred != barney?"
        except AssertionError:
            et, ev, tb = sys.exc_info()
            out = inspect_traceback(tb)
            # print "'%s'" % out.strip()
            self.assertEqual(out.strip(),
                             ">>  assert defred('fred') == 'barney', " 
                             '"Fred - fred != barney?"')
        try:
            val = "fred"
            def defred(n):
                return n.replace('fred','')
            assert defred(val) == 'barney', \
                "Fred - fred != barney?"
            def refred(n):
                return n + 'fred'
        except AssertionError:
            et, ev, tb = sys.exc_info()
            out = inspect_traceback(tb)
            #print "'%s'" % out.strip()
            self.assertEqual(out.strip(),
                             ">>  assert defred('fred') == 'barney', " 
                             '\\\n        "Fred - fred != barney?"')

        S = {'setup':1}
        def check_even(n, nn):
            assert S['setup']
            print n, nn
            assert n % 2 == 0 or nn % 2 == 0
        try:
            check_even(1, 3)
        except AssertionError:
            et, ev, tb = sys.exc_info()
            out = inspect_traceback(tb)
            print "'%s'" % out.strip()
            if sys.version_info < (3,):
                print_line = "    print 1, 3\n"
            else:
                print_line = "    print(1, 3)\n"
            self.assertEqual(out.strip(),
                             "assert {'setup': 1}['setup']\n" +
                             print_line +
                             ">>  assert 1 % 2 == 0 or 3 % 2 == 0")
            
    def test_bug_95(self):
        """Test that inspector can handle multi-line docstrings"""
        try:
            """docstring line 1
            docstring line 2
            """
            a = 2
            assert a == 4
        except AssertionError:
            et, ev, tb = sys.exc_info()
            out = inspect_traceback(tb)
            print "'%s'" % out.strip()
            self.assertEqual(out.strip(),
                             "2 = 2\n"
                             ">>  assert 2 == 4")
        
if __name__ == '__main__':
    #import logging
    #logging.basicConfig()
    #logging.getLogger('').setLevel(10)
    unittest.main()
    
