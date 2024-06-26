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
            tags middleware
            ards ards
            docs docs
            """,
            DslModule(
                body=[
                    DslProperty(id="tags", argument="middleware"),
                    DslProperty(id="ards", argument="ards"),
                    DslProperty(id="docs", argument="docs"),
                ]
            ),
            marks=pytest.mark.basic,
            id="Many_instructions",
        ),
        pytest.param(
            """
            filesystem = container filesystem {
                tags middleware
                !ards ards
                docs docs
                url https://examp-le.com
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
                            DslProperty(id="docs", argument="docs"),
                            DslProperty(id="url", argument="https://examp-le.com"),
                        ],
                    )
                ]
            ),
            marks=pytest.mark.basic,
            id="Many_instructions_in_node",
        ),
        pytest.param(
            """
            tags middleware
            blocks = container blocks {
                some_component_id = component some_component
            }
            """,
            DslModule(
                body=[
                    DslProperty(id="tags", argument="middleware"),
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
                    ),
                ]
            ),
            marks=pytest.mark.basic,
            id="Property_and_nodes",
        ),
        pytest.param(
            """
            blocks = container blocks {
                !tags "Tag1, Tag2"
                some_component_id = component some_component
            }
            """,
            DslModule(
                body=[
                    DslNode(
                        id="blocks",
                        descriptors=["container", "blocks"],
                        children=[
                            DslProperty(id="!tags", argument='"Tag1, Tag2"'),
                            DslNode(
                                id="some_component_id",
                                descriptors=["component", "some_component"],
                                children=[],
                            ),
                        ],
                    )
                ]
            ),
            marks=pytest.mark.basic,
            id="Property_and_nodes_in_nodes",
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
            id="Container with components",
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
            var_name = descriptor param1 param2
            other_name = component other_component
            comp_name = component some_component
            """,
            DslModule(
                body=[
                    DslNode(
                        id="var_name",
                        descriptors=["descriptor", "param1", "param2"],
                        children=[],
                    ),
                    DslNode(
                        id="other_name",
                        descriptors=["component", "other_component"],
                        children=[],
                    ),
                    DslNode(
                        id="comp_name",
                        descriptors=["component", "some_component"],
                        children=[],
                    ),
                ]
            ),
            marks=pytest.mark.basic,
            id="Many_simple_nodes",
        ),
        pytest.param(
            """
            var_name = descriptor param1 param2 {
                other_name = component other_component
                comp_name = component some_component
            }
            """,
            DslModule(
                body=[
                    DslNode(
                        id="var_name",
                        descriptors=["descriptor", "param1", "param2"],
                        children=[
                            DslNode(
                                id="other_name",
                                descriptors=["component", "other_component"],
                                children=[],
                            ),
                            DslNode(
                                id="comp_name",
                                descriptors=["component", "some_component"],
                                children=[],
                            ),
                        ],
                    ),
                ]
            ),
            marks=pytest.mark.basic,
            id="Many_nodes_in_children",
        ),
        pytest.param(
            """
            first = container first {
                second = component second {
                    third = component third 
                }
            }
                    """,
            DslModule(
                body=[
                    DslNode(
                        id="first",
                        descriptors=["container", "first"],
                        children=[
                            DslNode(
                                id="second",
                                descriptors=["component", "second"],
                                children=[
                                    DslNode(
                                        id="third",
                                        descriptors=["component", "third"],
                                        children=[],
                                    )
                                ],
                            )
                        ],
                    )
                ]
            ),
            marks=pytest.mark.basic,
            id="Many_nested",
        ),
        pytest.param(
            """
            blocks = container "blocks" {
                !docs docs
                tags "middleware"
            }
            """,
            DslModule(
                body=[
                    DslNode(
                        id="blocks",
                        descriptors=["container", "blocks"],
                        children=[
                            DslProperty(id="!docs", argument="docs"),
                            DslProperty(id="tags", argument='"middleware"'),
                        ],
                    )
                ]
            ),
            marks=pytest.mark.basic,
            id="Parameters_in_quotes",
        ),
    ],
)
def test_parse_models(code, expected) -> None:
    assert DslParser()(code) == expected
