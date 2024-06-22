from src.domain.parser import DslParser
from src.domain.tree.module import C4Container, C4Module


def test_parse_models() -> None:
    code = """
filesystem = container "filesystem" {
    tags "middleware"
}
"""
    assert DslParser()(code) == C4Module(body=[C4Container(id='filesystem', name='filesystem', description=None, technology=None, tags=[], children=[])])