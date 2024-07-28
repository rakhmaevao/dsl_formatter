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
            id="Comments",
        ),
        pytest.param(
            """engee.blocks.block_repr_builder -> engee.blocks.mask_processor "Пересчитать маску" """,
            [
                Token(
                    value="engee.blocks.block_repr_builder",
                    address=Address(file_path="test", line=1),
                ),
                Token(value="->", address=Address(file_path="test", line=1)),
                Token(
                    value="engee.blocks.mask_processor",
                    address=Address(file_path="test", line=1),
                ),
                Token(
                    value='"Пересчитать маску"',
                    address=Address(file_path="test", line=1),
                ),
                Token(value="\n", address=Address(file_path="test", line=1)),
            ],
            id="connections",
        ),
    ],
)
def test_basic(code, expected) -> None:
    tokenizer = DslTokenizer()
    assert tokenizer.pre_tokenize(code, "test") == expected


@pytest.mark.parametrize(
    "code, expected",
    [
        pytest.param(
            """engee.blocks.block_repr_builder -> engee.blocks.mask_processor "Пересчитать маску" """,
            [],
            id="connections",
        ),
    ],
)
def test_define_types(code, expected) -> None:
    tokenizer = DslTokenizer()
    tokens = tokenizer.pre_tokenize(
        """engee.blocks.block_repr_builder -> engee.blocks.mask_processor "Пересчитать маску" """,
        "test",
    )
    assert tokenizer.define_types(tokens) == []
