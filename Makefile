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
	@python -c 'import argparse' 2>/dev/null || pip install argparse --use-mirrors

cssselect:
	@python -c 'import cssselect' 2>/dev/null || pip install cssselect>=0.7.1 --use-mirrors

coverage:
	@python -c 'import coverage' 2>/dev/null || pip install coverage==3.5.1 --use-mirrors

selenium:
	@python -c 'import selenium' 2>/dev/null || pip install selenium==2.28.0 --use-mirrors

unittest2:
	@python -c 'from unittest import skip' 2>/dev/null || pip install unittest2 --use-mirrors

flask:
	@python -c 'import flask' 2>/dev/null || pip install flask==0.7.2 --use-mirrors

lxml:
	@python -c 'import lxml' 2>/dev/null || pip install lxml>=3.1beta1 --use-mirrors

sphinx:
	@python -c 'import sphinx' 2>/dev/null || pip install sphinx==1.1.3 --use-mirrors

zopetestbrowser:
	@python -c 'import zope.testbrowser' 2>/dev/null || pip install zope.testbrowser==4.0.2 --use-mirrors

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
