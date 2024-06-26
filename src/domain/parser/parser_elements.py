from dataclasses import dataclass
from ..module import DslModule, DslNode, DslProperty
from pyparsing import (
    Combine,
    Forward,
    Group,
    OneOrMore,
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

_entity_id_pe = Word(alphas + "_")

_descriptor_pe = Word(alphas + "_" + nums)
_property_pe = Group(Word(alphas + "!") + Word(alphas + nums + "_" + "," + " " + '"'))(
    "property"
)
c4_node_pe = Forward()

c4_node_pe << (
    _entity_id_pe("entity_id")
    + Suppress("=")
    + Group(OneOrMore(_descriptor_pe))("entity_descriptors")
    + Optional(
        nested_expr(
            "{",
            "}",
            (_property_pe ^ c4_node_pe),
            ignore_expr=(c_style_comment),
        )
    )("children")
)
