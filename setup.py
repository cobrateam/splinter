from setuptools import setup, find_packages

setup(name='splinter',
      version='0.1',
      description='browser abstraction to access pages',
      long_description='',
      author='CobraTeam',
      author_email='andrewsmedina@gmail.com',
      packages=find_packages(),
      test_suite='nose.collector',
      install_requires=['selenium'],
      tests_require=['nose', 'coverage'],
      )
