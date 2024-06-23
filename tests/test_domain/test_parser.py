import pytest
from src.domain.parser import DslParser
from src.domain.module import C4Component, C4Container, C4Module, DslInstruction


@pytest.mark.parametrize(
    "code, expected",
    [
        # pytest.param(
        #     """
        #     filesystem = container "filesystem"
        #     """,
        #     C4Module(
        #         body=[
        #             C4Container(
        #                 id="filesystem",
        #                 name="filesystem",
        #                 description=None,
        #                 technology=None,
        #                 tags=[],
        #                 children=[],
        #             )
        #         ]
        #     ),
        #     marks=pytest.mark.basic,
        #     id="Simple container",
        # ),
        # pytest.param(
        #     """
        #     filesystem = container "filesystem" {
        #         tags "middleware, anotherTag"
        #     }
        #     """,
        #     C4Module(
        #         body=[
        #             C4Container(
        #                 id="filesystem",
        #                 name="filesystem",
        #                 description=None,
        #                 technology=None,
        #                 tags=["middleware", "anotherTag"],
        #                 children=[],
        #             )
        #         ]
        #     ),
        #     marks=pytest.mark.basic,
        #     id="Many tags",
        # ),
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
                some_component_id = component "BlockReprBuilder"
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
                                id="block_repr_builder",
                                name="BlockReprBuilder",
                                description=None,
                                technology=None,
                                tags=["domain_layer"],
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
