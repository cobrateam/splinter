# -*- coding: utf-8 -*-
import argparse

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
    env.process = Process(target=start_flask_app, args=(env.host, env.port))
    env.process.daemon = True
    env.process.start()
    wait_until_start()


def stop_server():
    env.process.terminate()
    env.process.join()
    wait_until_stop()

if __name__ == '__main__':
    args = parser.parse_args()
    print args
    start_server()
    stop_server()
