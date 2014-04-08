#!/usr/bin/env python

# Copyright 2013 splinter authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

# -*- coding: utf-8 -*-

import argparse
import sys
import unittest
import os

from multiprocessing import Process
try:
    from urllib import urlopen
except ImportError:
    from urllib.request import urlopen

from tests import TESTS_ROOT
from tests.fake_webapp import start_flask_app, EXAMPLE_APP

parser = argparse.ArgumentParser('Run splinter tests')
parser.add_argument('-w', '--which', action='store')
parser.add_argument('-f', '--failfast', action='store_true')
parser.add_argument('-v', '--verbosity', type=int, default=1)


class Env(object):
    pass


env = Env()
env.process = None
env.host, env.port = 'localhost', 5000


def wait_until_start():
    while True:
        try:
            results = urlopen(EXAMPLE_APP)
            if results.code == 404:
                raise Exception('%s returned unexpected 404' % EXAMPLE_APP)
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
            print('Error importing module {}:'.format(name))
            import traceback
            traceback.print_exception(exc_type, exc_value, exc_traceback,
                                      file=sys.stdout)
        modules.append(module)

    return modules


def run_suite(suite, args):
    runner = unittest.TextTestRunner(sys.stdout, True, args.verbosity,
                                     args.failfast)
    return runner.run(suite)


def get_suite_from_modules(modules):
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    for module in modules:
        suite.addTest(loader.loadTestsFromModule(module))

    return suite


def get_complete_suite():
    loader = unittest.TestLoader()
    return loader.discover(
        start_dir=TESTS_ROOT,
        top_level_dir=os.path.join(TESTS_ROOT, os.path.pardir)
    )


if __name__ == '__main__':
    try:
        start_server()
    except Exception as e:
        sys.stdout.write("Failed to start test server: %s\n\n" % e)
        sys.exit(1)

    args = parser.parse_args()

    loader = unittest.TestLoader()
    if args.which and args.which != 'tests':
        modules = get_modules(args.which)
        suite = get_suite_from_modules(modules)
    else:
        suite = get_complete_suite()

    result = run_suite(suite, args)
    stop_server()
    sys.exit(len(result.errors) + len(result.failures))
