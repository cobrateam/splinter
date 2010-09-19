clean:
	@find . -name "*.pyc" -delete
	
dependencies: specloud coverage selenium ludibrio flask

specloud:
	@python -c 'import specloud' 2>/dev/null || pip install --no-deps specloud -r http://github.com/hugobr/specloud/raw/master/requirements.txt

coverage:
	@python -c 'import coverage' 2>/dev/null || pip install coverage

selenium:
	@python -c 'import selenium' 2>/dev/null || pip install selenium

ludibrio:
	@python -c 'import ludibrio' 2>/dev/null || pip install ludibrio

flask:
	@python -c 'import flask' 2>/dev/null || pip install flask


unit: dependencies clean
	@echo "Running unit tests..."
	specloud --nocapture --with-coverage --cover-erase --cover-inclusive --cover-package=splinter tests/unit


functional: dependencies clean
	@echo "Running functional tests..."
	python tests/functional/fake_webapp.py &
	specloud --nocapture --with-coverage --cover-erase --cover-inclusive --cover-package=splinter tests/functional
	kill -9 `ps aux | grep 'python tests/functional/fake_webapp.py' | grep -v grep | awk '{print $$2}'`


test:
	@echo "Running all tests..."
	python tests/functional/fake_webapp.py &
	specloud --nocapture --with-coverage --cover-erase --cover-inclusive --cover-package=splinter tests
	kill -9 `ps aux | grep 'python tests/functional/fake_webapp.py' | grep -v grep | awk '{print $$2}'`

