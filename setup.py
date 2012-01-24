from setuptools import setup, find_packages
from splinter import __version__

README = open('README.rst').read()

setup(name='splinter',
      version=__version__,
      description='browser abstraction for web acceptance testing',
      long_description=README,
      author='CobraTeam',
      author_email='andrewsmedina@gmail.com',
      packages=find_packages(exclude=['docs', 'tests', 'samples']),
      include_package_data=True,
      install_requires=['selenium==2.17', 'lxml>=2.3.1,<2.4.0'],
      tests_require=['coverage', 'flask'],
      )
