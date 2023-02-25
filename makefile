install:
	pip install --upgrade pip
	pip install -r requirements.txt
	pip install -r requirements-test.txt
test:
	pytest tests/
format:
	black main.py
	black src/
	black tests/
