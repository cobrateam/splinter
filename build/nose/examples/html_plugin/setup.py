import sys
try:
    import ez_setup
    ez_setup.use_setuptools()
except ImportError:
    pass

from setuptools import setup

setup(
    name='Example html output plugin',
    version='0.1',
    author='Jason Pellerin',
    author_email = 'jpellerin+nose@gmail.com',
    description = 'Example nose html output plugin',
    license = 'GNU LGPL',
    py_modules = ['htmlplug'],
    entry_points = {
        'nose.plugins.0.10': [
            'htmlout = htmlplug:HtmlOutput'
            ]
        }

    )
