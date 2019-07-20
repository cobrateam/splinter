# Copyright 2013 splinter authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

all: test

clean:
	@find . -name "*.pyc" -delete

doc_dependencies:
	@pip install -r doc-requirements.txt

dependencies:
	@pip install -r test-requirements.txt

doc: doc_dependencies
	@cd docs && make clean && make html

release:
	@sed -ic -e s/`cat VERSION`/$(version)/ setup.py docs/conf.py splinter/__init__.py
	@echo $(version) > VERSION
	@git add setup.py docs/conf.py VERSION splinter/__init__.py
	@git commit -m "setup: bump to $(version)"
	@git tag $(version)
	@git push --tags
	@git push origin master
	@rm dist/*
	@python setup.py sdist bdist_wheel
	@twine upload dist/*

which = 'tests'

test: dependencies clean
	@echo "Running all tests..."
	tox -- $(which)

format: clean dependencies
	@flake8 --max-line-length 110 ./splinter ./tests

coverage: dependencies clean
	@echo "Running all tests with coverage..."
	@coverage run run_tests.py -w $(which) && coverage report

install-remote:
	@wget http://goo.gl/PJUZfa -O selenium-server.jar
	@java -jar selenium-server.jar > /dev/null 2>&1 &
	@sleep 1
