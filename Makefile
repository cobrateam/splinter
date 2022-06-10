# Copyright 2013 splinter authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

all: test

clean:
	@find . -name "*.pyc" -delete

doc_dependencies:
	@pip install -r requirements/doc.txt

dependencies:
	@pip install -r requirements/test.txt

doc: doc_dependencies
	@cd docs && make clean && make html

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
