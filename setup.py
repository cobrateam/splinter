from setuptools import setup, find_packages

README = open('README.rst').read()

setup(name='splinter',
      version='0.4.4',
      description='browser abstraction for web acceptance testing',
      long_description=README,
      author='CobraTeam',
      author_email='andrewsmedina@gmail.com',
      packages=find_packages(exclude=['docs', 'tests', 'samples']),
      include_package_data=True,
      install_requires=['selenium==2.20.0', 'lxml>=2.3.1,<2.4.0'],
      tests_require=['coverage', 'flask'],
      )
