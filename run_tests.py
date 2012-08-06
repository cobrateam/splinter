#!/usr/bin/env python

# Copyright 2012 splinter authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

# -*- coding: utf-8 -*-
import argparse
import sys

try:
    import unittest2 as unittest
except ImportError, e:
    import unittest

from multiprocessing import Process
from urllib import urlopen

from tests import TESTS_ROOT
from tests.fake_webapp import start_flask_app, EXAMPLE_APP

parser = argparse.ArgumentParser('Run splinter tests')
parser.add_argument('-w', '--which', action='store')
parser.add_argument('-f', '--failfast', action='store_true')


class Env(object):
    pass


env = Env()
env.process = None
env.host, env.port = 'localhost', 5000


def wait_until_start():
    while True:
        try:
            urlopen(EXAMPLE_APP)
            break
        except IOError:
            pass


def wait_until_stop():
    while True:
        try:
            results = urlopen(EXAMPLE_APP)
            if results.code == 404:
                break
        except IOError:
            break


def start_server():
    sys.stderr = open('/dev/null', 'w')
    env.process = Process(target=start_flask_app, args=(env.host, env.port))
    env.process.daemon = True
    env.process.start()
    wait_until_start()


def stop_server():
    env.process.terminate()
    env.process.join()
    wait_until_stop()


def get_modules(modules_str):
    names = modules_str.split(',')
    modules = []

    for name in names:
        name = name.replace('/', '.').replace('.py', '')
        try:
            module = __import__(name, fromlist='tests')
        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            print 'Error importing module %s:' % name
            import traceback
            traceback.print_exception(exc_type, exc_value, exc_traceback,
                                      file=sys.stdout)
        modules.append(module)

    return modules


def get_result(args):
    result = unittest.TextTestResult(sys.stdout, descriptions=True, verbosity=1)

    if args.failfast:
        result.failfast = True

    return result


def run_suite(suite, result):
    suite.run(result)

    sys.stdout.write("\n\n")


def get_suite_from_modules(modules):
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    for module in modules:
        suite.addTest(loader.loadTestsFromModule(module))

    return suite


def get_complete_suite():
    loader = unittest.TestLoader()
    return loader.discover(TESTS_ROOT)


def print_errors(result):
    if result.errors:
        sys.stdout.write("\nERRORS\n\n")
        for method, trace in result.errors:
            sys.stdout.write("Test method: %s\n" % method)
            sys.stdout.write("%s" % trace)
            sys.stdout.write("=" * 120)
            sys.stdout.write("\n\n")


def print_failures(result):
    if result.failures:
        sys.stdout.write("\nFAILURES\n\n")
        for method, trace in result.failures:
            sys.stdout.write("Test method: %s\n" % method)
            sys.stdout.write("%s" % trace)
            sys.stdout.write("=" * 120)
            sys.stdout.write("\n\n")

if __name__ == '__main__':
    start_server()

    args = parser.parse_args()

    loader = unittest.TestLoader()
    if args.which and args.which != 'tests':
        modules = get_modules(args.which)
        suite = get_suite_from_modules(modules)
    else:
        suite = get_complete_suite()

    result = get_result(args)
    run_suite(suite, result)
    print_failures(result)
    print_errors(result)
    sys.stdout.write("%d tests. %d failures. %d errors.\n\n" % (result.testsRun, len(result.failures), len(result.errors)))

    stop_server()
    sys.exit(not result.wasSuccessful())
