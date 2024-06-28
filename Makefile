pytest:
	poetry run pytest -vv -s --disable-warnings tests/test_domain/test_parser.py -k "Many_nodes_in_children"

format:
	poetry run ruff format src tests