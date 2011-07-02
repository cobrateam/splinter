clean:
	@find . -name "*.pyc" -delete

doc_dependencies: sphinx

dependencies: nose coverage selenium flask lxml zopetestbrowser

doc: doc_dependencies
	@cd docs && make clean && make html

nose:
	@python -c 'import nose' 2>/dev/null || pip install nose

coverage:
	@python -c 'import coverage' 2>/dev/null || pip install coverage

selenium:
	@python -c 'import selenium' 2>/dev/null || pip install -U selenium==2.0rc3

flask:
	@python -c 'import flask' 2>/dev/null || pip install flask

lxml:
	@python -c 'import lxml' 2>/dev/null || pip install lxml

sphinx:
	@python -c 'import sphinx' 2>/dev/null || pip install sphinx

zopetestbrowser:
	@python -c 'import zope.testbrowser' 2>/dev/null || pip install zope.testbrowser

which = 'tests'

test: dependencies clean
	@echo "Running all tests..."
	@nosetests --nocapture --with-coverage --cover-erase --cover-inclusive --cover-package=splinter --tests=$(which)
