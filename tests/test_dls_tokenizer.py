import pytest
from dsl_token import PreToken, Address
from dsl_tokenizer import DslTokenizer


@pytest.mark.parametrize(
    "code, expected",
    [
        pytest.param(
            """filesystem = container filesystem""",
            [
                PreToken(value="filesystem", address=Address(file_path="test", line=1)),
                PreToken(value="=", address=Address(file_path="test", line=1)),
                PreToken(value="container", address=Address(file_path="test", line=1)),
                PreToken(value="filesystem", address=Address(file_path="test", line=1)),
                PreToken(value="\n", address=Address(file_path="test", line=1)),
            ],
            marks=pytest.mark.basic,
            id="Simple container",
        ),
        pytest.param(
            """filesystem = container filesystem {
                tags "Tag1, Tag2"
            }""",
            [
                PreToken(value="filesystem", address=Address(file_path="test", line=1)),
                PreToken(value="=", address=Address(file_path="test", line=1)),
                PreToken(value="container", address=Address(file_path="test", line=1)),
                PreToken(value="filesystem", address=Address(file_path="test", line=1)),
                PreToken(value="{", address=Address(file_path="test", line=1)),
                PreToken(value="\n", address=Address(file_path="test", line=1)),
                PreToken(value="tags", address=Address(file_path="test", line=2)),
                PreToken(
                    value='"Tag1, Tag2"', address=Address(file_path="test", line=2)
                ),
                PreToken(value="\n", address=Address(file_path="test", line=2)),
                PreToken(value="}", address=Address(file_path="test", line=3)),
                PreToken(value="\n", address=Address(file_path="test", line=3)),
            ],
            id="Many tags",
        ),
        pytest.param(
            """filesystem
            # Comment
            // Comment""",
            [
                PreToken(value="filesystem", address=Address(file_path="test", line=1)),
                PreToken(value="\n", address=Address(file_path="test", line=1)),
                PreToken(value="# Comment", address=Address(file_path="test", line=2)),
                PreToken(value="\n", address=Address(file_path="test", line=2)),
                PreToken(value="// Comment", address=Address(file_path="test", line=3)),
                PreToken(value="\n", address=Address(file_path="test", line=3)),
            ],
            id="Many tags",
        ),
    ],
)
def test_basic(code, expected) -> None:
    tokenizer = DslTokenizer()
    assert tokenizer.tokenize(code, "test") == expected
