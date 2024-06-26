import pytest
from src.domain.code_generator import CodeGenerator
from src.domain.parser.parser import DslParser
from src.domain.module import C4Container, DslModule


@pytest.mark.parametrize(
    "module, expected",
    [
        (
            DslModule(
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
