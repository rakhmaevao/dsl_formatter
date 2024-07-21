pytest:
	poetry run pytest -vv -s --disable-warnings tests/test_dls_tokenizer.py
	
format:
	poetry run ruff format src tests