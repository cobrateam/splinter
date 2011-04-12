"""
An example of how to create a simple nose plugin.

"""
try:
    import ez_setup
    ez_setup.use_setuptools()
except ImportError:
    pass

from setuptools import setup

setup(
    name='Example plugin',
    version='0.1',
    author='Jason Pellerin',
    author_email = 'jpellerin+nose@gmail.com',
    description = 'Example nose plugin',
    license = 'GNU LGPL',
    py_modules = ['plug'],
    entry_points = {
        'nose.plugins.0.10': [
            'example = plug:ExamplePlugin'
            ]
        }

    )
