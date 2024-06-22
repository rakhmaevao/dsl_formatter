import pytest
from src.domain.code_generator import CodeGenerator
from src.domain.parser import DslParser
from src.domain.module import C4Container, C4Module


@pytest.mark.parametrize(
    "module, expected",
    [
        (
            C4Module(
                body=[
                    C4Container(
                        id="filesystem",
                        name="filesystem",
                        description=None,
                        technology=None,
                        tags="middleware",
                        children=[],
                    )
                ]
            ),
            """filesystem = container "filesystem" {
    tags "middleware"
}""",
        ),
    ],
)
def test_parse_models(module, expected) -> None:
    assert CodeGenerator()(module) == expected
