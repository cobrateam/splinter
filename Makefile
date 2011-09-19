clean:
	@find . -name "*.pyc" -delete

doc_dependencies: sphinx

dependencies: nose coverage selenium flask lxml zopetestbrowser

doc: doc_dependencies
	@cd docs && make clean && make html

nose:
	@python -c 'import nose' 2>/dev/null || pip install nose==1.1.2

coverage:
	@python -c 'import coverage' 2>/dev/null || pip install coverage==3.5

selenium:
	@python -c 'import selenium' 2>/dev/null || pip install -U selenium==2.6.0

flask:
	@python -c 'import flask' 2>/dev/null || pip install flask==0.7.2

lxml:
	@python -c 'import lxml' 2>/dev/null || pip install lxml==2.3

sphinx:
	@python -c 'import sphinx' 2>/dev/null || pip install sphinx==1.0.7

zopetestbrowser:
	@python -c 'import zope.testbrowser' 2>/dev/null || pip install zope.testbrowser==4.0.2

which = 'tests'

test: dependencies clean
	@echo "Running all tests..."
	@nosetests -s --with-coverage --cover-erase --cover-inclusive --cover-package=splinter --tests=$(which)
