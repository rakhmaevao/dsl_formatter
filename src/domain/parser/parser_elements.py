from dataclasses import dataclass
from ..module import DslModule, DslNode, DslProperty
from pyparsing import (
    Combine,
    Forward,
    Group,
    ParseResults,
    White,
    Word,
    ZeroOrMore,
    alphanums,
    alphas,
    Suppress,
    Optional,
    c_style_comment,
    nested_expr,
    nums,
)
from loguru import logger

_entity_id_pe = Word(alphas + "_")
_entity_type_pe = Word(alphas + "_")
_entity_name_pe = Word(alphas + "_")

_property_pe = Group(Word(alphas + "!") + Word(alphas + nums + "_" + "," + " " + '"'))
c4_node_pe = Forward()

c4_node_pe << (
    _entity_id_pe("entity_id")
    + Suppress("=")
    + _entity_type_pe("entity_type")
    + Suppress('"')
    + _entity_name_pe("entity_name")
    + Suppress('"')
    + Optional(
        nested_expr(
            "{",
            "}",
            (_property_pe ^ c4_node_pe),
            ignore_expr=(c_style_comment),
        )
    )("children")
)
