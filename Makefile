pytest:
	poetry run pytest -vv -s --disable-warnings tests

format:
	poetry run ruff format src tests