pytest:
	poetry run pytest -vv -s --disable-warnings tests/test_domain/test_parser.py -k "Many_instructions_in_node"

format:
	poetry run ruff format src tests