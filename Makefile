test: flake8 pylint pytest

flake8:
	flake8 nameko_management test

pylint:
	pylint nameko_management -E

pytest:
	coverage run --concurrency=eventlet --source nameko_management --branch -m pytest test
	coverage report --show-missing --fail-under=100
