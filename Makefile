# Copyright 2012 splinter authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

all: test

clean:
	@find . -name "*.pyc" -delete

doc_dependencies: sphinx

dependencies: unittest2 argparse coverage selenium flask lxml zopetestbrowser

doc: doc_dependencies
	@cd docs && make clean && make html

argparse:
	@python -c 'import argparse' 2>/dev/null || pip install argparse

coverage:
	@python -c 'import coverage' 2>/dev/null || pip install coverage==3.5.1

selenium:
	@python -c 'import selenium' 2>/dev/null || pip install selenium==2.25.0

unittest2:
	@python -c 'from unittest import skip' 2>/dev/null || pip install unittest2

flask:
	@python -c 'import flask' 2>/dev/null || pip install flask==0.7.2

lxml:
	@python -c 'import lxml' 2>/dev/null || pip install lxml==2.3.1

sphinx:
	@python -c 'import sphinx' 2>/dev/null || pip install sphinx==1.1.3

zopetestbrowser:
	@python -c 'import zope.testbrowser' 2>/dev/null || pip install zope.testbrowser==4.0.2

release:
	@sed -ic -e s/`cat VERSION`/$(version)/ setup.py docs/conf.py splinter/__init__.py
	@echo $(version) > VERSION
	@git add setup.py docs/conf.py VERSION splinter/__init__.py
	@git commit -m "setup: bump to $(version)"
	@git tag $(version)
	@git push --tags
	@git push origin master
	@python setup.py sdist upload

which = 'tests'

test: dependencies clean
	@echo "Running all tests..."
	@coverage run run_tests.py -w $(which)
	@coverage report
	@echo
