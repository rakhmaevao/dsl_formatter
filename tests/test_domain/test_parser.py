import pytest
from src.domain.parser import DslParser
from src.domain.module import C4Component, C4Container, C4Module, DslInstruction


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
                tags "Tag1, Tag2"
            }
            """,
            C4Module(
                body=[
                    C4Container(
                        id="filesystem",
                        name="filesystem",
                        description=None,
                        technology=None,
                        tags=["Tag1", "Tag2"],
                        children=[],
                    )
                ]
            ),
            marks=pytest.mark.basic,
            id="Many tags",
        ),
        # pytest.param(
        #     """
        #     filesystem = container "filesystem" {
        #         tags "middleware"
        #         !docs docs
        #         !ards ards
        #     }
        #     """,
        #     C4Module(
        #         body=[
        #             C4Container(
        #                 id="filesystem",
        #                 name="filesystem",
        #                 description=None,
        #                 technology=None,
        #                 tags=["middleware"],
        #                 children=[
        #                     DslInstruction(id="!docs", argument="docs"),
        #                     DslInstruction(id="!ards", argument="ards"),
        #                 ],
        #             )
        #         ]
        #     ),
        #     marks=pytest.mark.basic,
        #     id="Many !instructions",
        # ),
        pytest.param(
            """
            blocks = container "blocks" {
                some_component_id = component "SomeComponent" 
            }
            """,
            C4Module(
                body=[
                    C4Container(
                        id="blocks",
                        name="blocks",
                        description=None,
                        technology=None,
                        tags=[],
                        children=[
                            C4Component(
                                id="some_component_id",
                                name="SomeComponent",
                                description=None,
                                technology=None,
                                tags=[],
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
