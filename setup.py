from setuptools import setup
from splinter import __version__

README = open('README.rst').read()

setup(name='splinter',
      version=__version__,
      description='browser abstraction for web acceptance testing',
      long_description=README,
      author='CobraTeam',
      author_email='andrewsmedina@gmail.com',
      packages=['splinter'],
      include_package_data=True,
      install_requires=['selenium==2.13.1', 'lxml==2.3.1'],
      tests_require=['coverage', 'flask'],
      )
