import pytest
from dsl_token import Token, Address
from dsl_tokenizer import DslTokenizer


@pytest.mark.parametrize(
    "code, expected",
    [
        pytest.param(
            """filesystem = container filesystem""",
            [
                Token(value="filesystem", address=Address(file_path="test", line=1)),
                Token(value="=", address=Address(file_path="test", line=1)),
                Token(value="container", address=Address(file_path="test", line=1)),
                Token(value="filesystem", address=Address(file_path="test", line=1)),
                Token(value="\n", address=Address(file_path="test", line=1)),
            ],
            marks=pytest.mark.basic,
            id="Simple container",
        ),
        pytest.param(
            """filesystem = container filesystem {
                tags "Tag1, Tag2"
            }""",
            [
                Token(value="filesystem", address=Address(file_path="test", line=1)),
                Token(value="=", address=Address(file_path="test", line=1)),
                Token(value="container", address=Address(file_path="test", line=1)),
                Token(value="filesystem", address=Address(file_path="test", line=1)),
                Token(value="{", address=Address(file_path="test", line=1)),
                Token(value="\n", address=Address(file_path="test", line=1)),
                Token(value="tags", address=Address(file_path="test", line=2)),
                Token(value='"Tag1, Tag2"', address=Address(file_path="test", line=2)),
                Token(value="\n", address=Address(file_path="test", line=2)),
                Token(value="}", address=Address(file_path="test", line=3)),
                Token(value="\n", address=Address(file_path="test", line=3)),
            ],
            id="Many tags",
        ),
        pytest.param(
            """filesystem
            # Comment
            // Comment""",
            [
                Token(value="filesystem", address=Address(file_path="test", line=1)),
                Token(value="\n", address=Address(file_path="test", line=1)),
                Token(value="# Comment", address=Address(file_path="test", line=2)),
                Token(value="\n", address=Address(file_path="test", line=2)),
                Token(value="// Comment", address=Address(file_path="test", line=3)),
                Token(value="\n", address=Address(file_path="test", line=3)),
            ],
            id="Many tags",
        ),
    ],
)
def test_basic(code, expected) -> None:
    tokenizer = DslTokenizer()
    assert tokenizer.tokenize(code, "test") == expected
