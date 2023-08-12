# Set up Python Virtual Environment
setup-venv:
	python3.9 -m venv .venv
	. .venv/bin/activate

# Install Dependencies
install-deps: setup-venv
	. .venv/bin/activate && pip install -r requirements.txt

# Make script executable and run tests
test:
	chmod +x run_tests.sh
	./run_tests.sh

# Run linters and formatters (You might not need all these; adjust accordingly)
lint:
	. .venv/bin/activate && flake8
	. .venv/bin/activate && black --check .
	. .venv/bin/activate && isort --check-only .

format:
	. .venv/bin/activate && black .
	. .venv/bin/activate && isort .

# Clean up pycache files
clean:
	find . -name "__pycache__" -exec rm -rf {} +
	find . -name "*.pyc" -exec rm -f {} +
