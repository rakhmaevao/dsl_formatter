import pytest
from src.domain.parser.parser import DslParser
from src.domain.module import C4Module, C4Node, DslInstruction


@pytest.mark.parametrize(
    "code, expected",
    [
        pytest.param(
            """
            filesystem = container "filesystem"
            """,
            C4Module(
                body=[
                    C4Node(
                        id="filesystem",
                        type="container",
                        name="filesystem",
                        description=None,
                        technology=None,
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
                tags "Tag1, Tag2"
            }
            """,
            C4Module(
                body=[
                    C4Node(
                        id="filesystem",
                        type="container",
                        name="filesystem",
                        description=None,
                        technology=None,
                        children=[DslInstruction(id="tags", argument='"Tag1, Tag2"')],
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
                !ards ards
                !docs docs
            }
            """,
            C4Module(
                body=[
                    C4Node(
                        id="filesystem",
                        type="container",
                        name="filesystem",
                        description=None,
                        technology=None,
                        children=[
                            DslInstruction(id="tags", argument='"middleware"'),
                            DslInstruction(id="!ards", argument="ards"),
                            DslInstruction(id="!docs", argument="docs"),
                        ],
                    )
                ]
            ),
            marks=pytest.mark.basic,
            id="Many !instructions",
        ),
        pytest.param(
            """
            blocks = container "blocks" {
                some_component_id = component "SomeComponent" 
            }
            """,
            C4Module(
                body=[
                    C4Node(
                        id="blocks",
                        type="container",
                        name="blocks",
                        description=None,
                        technology=None,
                        children=[
                            C4Node(
                                id="some_component_id",
                                type="component",
                                name="SomeComponent",
                                description=None,
                                technology=None,
                                children=[],
                            )
                        ],
                    )
                ]
            ),
            marks=pytest.mark.basic,
            id="Container with components",
        ),
    ],
)
def test_parse_models(code, expected) -> None:
    assert DslParser()(code) == expected
