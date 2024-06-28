from dataclasses import dataclass
from ..module import DslModule, DslNode, DslProperty
from pyparsing import (
    Char,
    Combine,
    Forward,
    Group,
    LineEnd,
    LineStart,
    OneOrMore,
    ParseResults,
    ParserElement,
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

# ParserElement.set_default_whitespace_chars(' \t')

_entity_id_pe = Word(alphas + "_")

_descriptor_pe = Word(alphas + "_" + nums)
_property_pe = Group(Word(alphas + "!" + "_") + Word(alphas + nums + "_"))("property")

ParserElement.set_default_whitespace_chars("")
_children_pe = OneOrMore(Word(alphanums + "_" + " " + "=" + "\n"))
ParserElement.set_default_whitespace_chars(" ")


c4_node_pe = OneOrMore(
    Suppress(ZeroOrMore("\n"))
    + Group(
        _entity_id_pe("entity_id")
        + Suppress("=")
        + Group(OneOrMore(_descriptor_pe, stop_on=(LineEnd() | "{")))(
            "entity_descriptors"
        )
        + (
            Suppress("\n")
            | nested_expr(
                "{",
                "}",
                _children_pe,
                ignore_expr=(c_style_comment),
            )("children")
        )
    )
)
