#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import sys
import unittest

from multiprocessing import Process
from urllib import urlopen

from tests.fake_webapp import start_flask_app, EXAMPLE_APP

parser = argparse.ArgumentParser('Run splinter tests')
parser.add_argument('-w', '--which', action='store')


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
        modules.append(__import__(name, fromlist='tests'))

    return modules


def run_tests_from_modules(modules, result):
    loader = unittest.TestLoader()
    for module in modules:
        suite = loader.loadTestsFromModule(module)
        suite.run(result)

    sys.stdout.write("\n\n")

    return result

def run_all_tests(result):
    pass

def print_errors(result):
    if result.errors:
        sys.stdout.write("\nERRORS\n\n")
        for method, trace in result.errors:
            sys.stdout.write("Test method: %s\n" % method)
            sys.stdout.write("%s" % trace)
            sys.stdout.write("="*120)
            sys.stdout.write("\n\n")

def print_failures(result):
    if result.failures:
        sys.stdout.write("\nFAILURES\n\n")
        for method, trace in result.failures:
            sys.stdout.write("Test method: %s\n" % method)
            sys.stdout.write("%s" % trace)
            sys.stdout.write("="*120)
            sys.stdout.write("\n\n")

if __name__ == '__main__':
    start_server()

    args = parser.parse_args()
    result = unittest.TextTestResult(sys.stdout, descriptions=True, verbosity=1)

    loader = unittest.TestLoader()
    if args.which and args.which != 'tests':
        modules = get_modules(args.which)
        run_tests_from_modules(modules, result)
    else:
        run_all_tests(result)

    print_failures(result)
    print_errors(result)
    sys.stdout.write("Ran %d tests, %d failures, %d errors.\n" % (result.testsRun, len(result.failures), len(result.errors)))

    stop_server()
    sys.exit(not result.wasSuccessful())
