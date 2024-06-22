import pytest
from src.domain.parser import DslParser
from src.domain.module import C4Container, C4Module, DslInstruction


@pytest.mark.parametrize(
    "code, expected",
    [
        (
            """
            filesystem = container "filesystem" {
                tags "middleware"
            }
            """,
            C4Module(
                body=[
                    C4Container(
                        id="filesystem",
                        name="filesystem",
                        description=None,
                        technology=None,
                        tags=["middleware"],
                        children=[],
                    )
                ]
            ),
        ),
        (
            """
            filesystem = container "filesystem" {
                tags "middleware"
                !docs docs
            }
            """,
            C4Module(
                body=[
                    C4Container(
                        id="filesystem",
                        name="filesystem",
                        description=None,
                        technology=None,
                        tags=["middleware"],
                        children=[
                            DslInstruction(id="!docs", argument="docs"),
                        ],
                    )
                ]
            ),
        ),
    ],
)
def test_parse_models(code, expected) -> None:
    assert DslParser()(code) == expected
