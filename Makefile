all: test

clean:
	@find . -name "*.pyc" -delete

dependencies: specloud coverage selenium flask lxml sphinx zopetestbrowser

doc:
	@cd docs && make clean && make html

specloud:
	@python -c 'import specloud' 2>/dev/null || pip install specloud

coverage:
	@python -c 'import coverage' 2>/dev/null || pip install coverage

selenium:
	@python -c 'import selenium' 2>/dev/null || pip install -U selenium==2.0rc2

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
	specloud --nocapture --with-coverage --cover-erase --cover-inclusive --cover-package=splinter --tests=$(which)

