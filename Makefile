pytest:
	poetry run pytest -vv -s --disable-warnings tests/test_domain/test_parser.py -k "Container_with_components"
format:
	poetry run ruff format src tests