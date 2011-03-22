all: test

clean:
	@find . -name "*.pyc" -delete

dependencies: specloud coverage selenium flask shoulddsl lxml zopetestbrowser

specloud:
	@python -c 'import specloud' 2>/dev/null || pip install --no-deps specloud -r http://github.com/hugobr/specloud/raw/master/requirements.txt

coverage:
	@python -c 'import coverage' 2>/dev/null || pip install coverage

selenium:
	@python -c 'import selenium' 2>/dev/null || pip install -U selenium==2.0b3

flask:
	@python -c 'import flask' 2>/dev/null || pip install flask

shoulddsl:
	@python -c 'import should_dsl' 2>/dev/null || pip install should-dsl

lxml:
	@python -c 'import lxml' 2>/dev/null || pip install lxml

zopetestbrowser:
	@python -c 'import zope.testbrowser' 2>/dev/null || pip install zope.testbrowser

test: dependencies clean
	@echo "Running all tests..."
	specloud --nocapture --with-coverage --cover-erase --cover-inclusive --cover-package=splinter tests

