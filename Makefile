clean:
	@find . -name "*.pyc" -delete
	
dependencies: nose coverage selenium ludibrio

nose:
	@python -c 'import nose' 2>/dev/null || pip install nose

coverage:
	@python -c 'import coverage' 2>/dev/null || pip install coverage

selenium:
	@python -c 'import selenium' 2>/dev/null || pip install selenium

ludibrio:
	@python -c 'import ludibrio' 2>/dev/null || pip install ludibrio

test: dependencies clean
	@echo "Running tests..."
	nosetests --nocapture --verbosity=2 --with-coverage --cover-erase --cover-inclusive --cover-package=splinter tests

unit: dependencies clean
	@echo "Running unit tests..."
	nosetests --nocapture --verbosity=2 --with-coverage --cover-erase --cover-inclusive --cover-package=splinter tests/unit


functional: dependencies clean
	@echo "Running functional tests..."
	nosetests --nocapture --verbosity=2 --with-coverage --cover-erase --cover-inclusive --cover-package=splinter tests/functional
