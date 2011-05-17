from setuptools import setup, find_packages


README = open('README.rst').read()

setup(name='splinter',
      version='0.0.3',
      description='browser abstraction for web acceptance testing',
      long_description=README,
      author='CobraTeam',
      author_email='andrewsmedina@gmail.com',
      packages=find_packages(),
      include_package_data=True,
      test_suite='nose.collector',
      install_requires=['selenium==2.0b3', 'lxml'],
      tests_require=['nose', 'coverage', 'ludibrio', 'flask', 'specloud'],
      )
