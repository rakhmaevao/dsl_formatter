import pytest
from src.domain.parser import DslParser
from src.domain.module import DslModule, DslNode, DslProperty


@pytest.mark.parametrize(
    "code, expected",
    [
        # pytest.param(
        #     """
        #     filesystem = container "filesystem"
        #     """,
        #     DslModule(
        #         body=[
        #             DslNode(
        #                 id="filesystem",
        #                 type="container",
        #                 name="filesystem",
        #                 description=None,
        #                 technology=None,
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
        #         tags "Tag1, Tag2"
        #     }
        #     """,
        #     DslModule(
        #         body=[
        #             DslNode(
        #                 id="filesystem",
        #                 type="container",
        #                 name="filesystem",
        #                 description=None,
        #                 technology=None,
        #                 children=[DslProperty(id="tags", argument='"Tag1, Tag2"')],
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
        #         !ards ards
        #         !docs docs
        #     }
        #     """,
        #     DslModule(
        #         body=[
        #             DslNode(
        #                 id="filesystem",
        #                 type="container",
        #                 name="filesystem",
        #                 description=None,
        #                 technology=None,
        #                 children=[
        #                     DslProperty(id="tags", argument='"middleware"'),
        #                     DslProperty(id="!ards", argument="ards"),
        #                     DslProperty(id="!docs", argument="docs"),
        #                 ],
        #             )
        #         ]
        #     ),
        #     marks=pytest.mark.basic,
        #     id="Many !instructions",
        # ),
        pytest.param(
            """
            blocks = container blocks {
                some_component_id = component some_component
            }
            """,
            DslModule(
                body=[
                    DslNode(
                        id="blocks",
                        descriptors=["container", "blocks"],
                        children=[
                            DslNode(
                                id="some_component_id",
                                descriptors=["component", "some_component"],
                                children=[],
                            )
                        ],
                    )
                ]
            ),
            marks=pytest.mark.basic,
            id="Container with components",
        ),
        # pytest.param(
        #     """
        #     var_name = descriptor param1 param2 param3 param4
        #     """,
        #     DslModule(
        #         body=[
        #             DslNode(
        #                 id="var_name",
        #                 descriptors=[
        #                     "descriptor",
        #                     "param1",
        #                     "param2",
        #                     "param3",
        #                     "param4",
        #                 ],
        #                 children=[],
        #             )
        #         ]
        #     ),
        #     marks=pytest.mark.basic,
        #     id="Many params",
        # ),
    ],
)
def test_parse_models(code, expected) -> None:
    assert DslParser()(code) == expected
