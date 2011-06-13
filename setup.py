from setuptools import setup, find_packages
from splinter import __version__

README = open('README.rst').read()

setup(name='splinter',
      version=__version__,
      description='browser abstraction for web acceptance testing',
      long_description=README,
      author='CobraTeam',
      author_email='andrewsmedina@gmail.com',
      packages=find_packages(),
      include_package_data=True,
      test_suite='nose.collector',
      install_requires=['selenium==2.0rc2', 'lxml'],
      tests_require=['nose', 'coverage', 'ludibrio', 'flask', 'specloud'],
      )
