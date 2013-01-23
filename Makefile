# Copyright 2012 splinter authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

all: test

clean:
	@find . -name "*.pyc" -delete

doc_dependencies: sphinx

dependencies:
	@pip install -r test-requirements.txt --use-mirrors

doc: doc_dependencies
	@cd docs && make clean && make html

sphinx:
	@python -c 'import sphinx' 2>/dev/null || pip install sphinx==1.1.3 --use-mirrors

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
