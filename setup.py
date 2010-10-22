from setuptools import setup, find_packages

setup(name='splinter',
      version='0.1',
      description='browser abstraction for web acceptance testing',
      long_description='',
      author='CobraTeam',
      author_email='andrewsmedina@gmail.com',
      packages=find_packages(),
      test_suite='nose.collector',
      install_requires=['selenium', 'zope.testbrowser'],
      tests_require=['nose', 'coverage', 'ludibrio', 'flask'],
      )
