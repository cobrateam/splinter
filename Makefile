clean:
	@find . -name "*.pyc" -delete
	
test: clean
	@echo "Running tests..."
	python setup.py test
