from setuptools import setup, find_packages

setup(
    name='Some plugin',
    packages = find_packages(),
    entry_points = {
    'nose.plugins.0.10': [
    'someplugin = someplugin:SomePlugin'
    ]
    })
