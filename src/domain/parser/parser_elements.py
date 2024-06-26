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

_variable_name = Word(alphanums + "_")
_descriptor_pe = Word(alphanums + "_")
_property_pe = Group(
    Word(alphanums + "_" + "!")("property_name")
    + Word(alphanums + "_")("property_value")
)("property")

c4_node_pe = Forward()

_node_extension_pe = (
    Suppress("{") + ZeroOrMore(_property_pe ^ c4_node_pe) + Suppress("}")
)

c4_node_pe << (
    _variable_name("entity_id")
    + Suppress("=")
    + Group(OneOrMore(_descriptor_pe))("entity_descriptors")
    + Optional(_node_extension_pe)("children")
)
