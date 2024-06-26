import pytest
from src.domain.parser import DslParser
from src.domain.module import DslModule, DslNode, DslProperty


@pytest.mark.parametrize(
    "code, expected",
    [
        pytest.param(
            """
            filesystem = container filesystem
            """,
            DslModule(
                body=[
                    DslNode(
                        id="filesystem",
                        descriptors=["container", "filesystem"],
                        children=[],
                    )
                ]
            ),
            marks=pytest.mark.basic,
            id="Simple container",
        ),
        pytest.param(
            """
            filesystem = container filesystem {
                tags "Tag1, Tag2"
            }
            """,
            DslModule(
                body=[
                    DslNode(
                        id="filesystem",
                        descriptors=["container", "filesystem"],
                        children=[DslProperty(id="tags", argument='"Tag1, Tag2"')],
                    )
                ]
            ),
            marks=pytest.mark.skip(reason="Пока не могу в двойные кавычки"),
            id="Many tags",
        ),
        pytest.param(
            """
            filesystem = container filesystem {
                tags middleware
                !ards ards
                !docs docs
            }
            """,
            DslModule(
                body=[
                    DslNode(
                        id="filesystem",
                        descriptors=["container", "filesystem"],
                        children=[
                            DslProperty(id="tags", argument="middleware"),
                            DslProperty(id="!ards", argument="ards"),
                            DslProperty(id="!docs", argument="docs"),
                        ],
                    )
                ]
            ),
            marks=pytest.mark.basic,
            id="Many_instructions",
        ),
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
            id="Container_with_components",
        ),
        pytest.param(
            """
            var_name = descriptor param1 param2 param3 param4
            """,
            DslModule(
                body=[
                    DslNode(
                        id="var_name",
                        descriptors=[
                            "descriptor",
                            "param1",
                            "param2",
                            "param3",
                            "param4",
                        ],
                        children=[],
                    )
                ]
            ),
            marks=pytest.mark.basic,
            id="Many descriptors",
        ),
        pytest.param(
            """
            var_name = descriptor param1 param2 {
                prop_id prop_value
            }
            """,
            DslModule(
                body=[
                    DslNode(
                        id="var_name",
                        descriptors=[
                            "descriptor",
                            "param1",
                            "param2",
                        ],
                        children=[DslProperty(id="prop_id", argument="prop_value")],
                    )
                ]
            ),
            marks=pytest.mark.basic,
            id="Many_descriptors_with_child",
        ),
        pytest.param(
            """
            var_name = descriptor param1 {
                other_var_name = descriptor param
                var_name = descriptor param
            }
            """,
            DslModule(
                body=[
                    DslNode(
                        id="var_name",
                        descriptors=[
                            "descriptor",
                            "param1",
                        ],
                        children=[
                            DslProperty(id="prop_id", argument="prop_value"),
                            DslNode(
                                id="var_name_1",
                                descriptors=[
                                    "descriptor1",
                                    "param1",
                                ],
                                children=[],
                            ),
                            DslNode(
                                id="var_name_2",
                                descriptors=[
                                    "descriptor2",
                                    "param2",
                                ],
                                children=[],
                            ),
                        ],
                    )
                ]
            ),
            marks=pytest.mark.basic,
            id="Many_node_children",
        ),
    ],
)
def test_parse_models(code, expected) -> None:
    assert DslParser()(code) == expected
