from setuptools import setup, find_packages
import os

version = '0.4.2'
here = os.path.abspath(os.path.dirname(__file__))
long_description = open(os.path.join(here, 'README.rst')).read()

setup(name='specloud',
      version=version,
      description="install nosetests and plugins to ease bdd unit specs",
      long_description=long_description,
      classifiers=[
      'Development Status :: 4 - Beta',
      'Environment :: Console',
      'Intended Audience :: Developers',
      'License :: OSI Approved :: MIT License',
      'Natural Language :: English',
      'Natural Language :: Portuguese (Brazilian)',
      'Operating System :: OS Independent',
      'Topic :: Software Development :: Testing',
      'Topic :: Utilities',
      ],
      keywords='test bdd nosetests spec unit',
      author='Hugo Lopes Tavares',
      author_email='hltbra@gmail.com',
      url='http://github.com/hugobr/specloud',
      license='MIT',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'nose',
          'figleaf',
          'pinocchio==0.2',
      ],
      dependency_links = [
          'http://darcs.idyll.org/~t/projects/pinocchio-latest.tar.gz#egg=pinocchio-0.2',
      ],
      entry_points="""
      [console_scripts]
      specloud = specloud:main
      """,
      )

