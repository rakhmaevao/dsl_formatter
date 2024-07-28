pytest:
	poetry run pytest -vv -s --disable-warnings tests/test_url_checker.py
	
format:
	poetry run ruff format src tests