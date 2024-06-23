import pytest
from src.domain.parser import DslParser
from src.domain.module import C4Container, C4Module, DslInstruction


@pytest.mark.parametrize(
    "code, expected",
    [
        pytest.param(
            """
            filesystem = container "filesystem"
            """,
            C4Module(
                body=[
                    C4Container(
                        id="filesystem",
                        name="filesystem",
                        description=None,
                        technology=None,
                        tags=[],
                        children=[],
                    )
                ]
            ),
            marks=pytest.mark.basic,
            id="Simple container",
        ),
        pytest.param(
            """
            filesystem = container "filesystem" {
                tags "middleware, anotherTag"
            }
            """,
            C4Module(
                body=[
                    C4Container(
                        id="filesystem",
                        name="filesystem",
                        description=None,
                        technology=None,
                        tags=["middleware", "anotherTag"],
                        children=[],
                    )
                ]
            ),
            marks=pytest.mark.basic,
            id="Many tags",
        ),
        pytest.param(
            """
            filesystem = container "filesystem" {
                tags "middleware"
                !docs docs
                !ards ards
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
                            DslInstruction(id="!ards", argument="ards"),
                        ],
                    )
                ]
            ),
            marks=pytest.mark.basic,
            id="Many !instructions",
        ),
    ],
)
def test_parse_models(code, expected) -> None:
    assert DslParser()(code) == expected
