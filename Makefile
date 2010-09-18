
clean:
	@find . -name "*.pyc" -delete
	
test: clean
	@echo "Running tests..."
	@nosetests -s --verbosity=2 --with-coverage --cover-erase --cover-inclusive tests/ --cover-package=splinter
