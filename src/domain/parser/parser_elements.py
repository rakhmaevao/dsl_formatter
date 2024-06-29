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

_entity_id_pe = Word(alphas + "_")

_descriptor_pe = Word(alphas + "_" + nums)


ParserElement.set_default_whitespace_chars("")
_children_pe = OneOrMore(
    Word(alphanums + "_" + " " + "=" + "\n" + "!" + '"' + "," + "/" + ":" + "-" + ".")
)
ParserElement.set_default_whitespace_chars(" ")
_property_pe = Group(
    Word(alphas + "!" + "_")("property_name")
    + Word(alphas + nums + "_" + '"' + "," + " " + "/" + ":" + "-" + ".")(
        "property_value"
    )
    + Suppress("\n")
)("property")

c4_node_pe = OneOrMore(
    (Suppress(ZeroOrMore("\n")) + _property_pe)
    ^ (
        Suppress(ZeroOrMore("\n"))
        + Group(
            _entity_id_pe("entity_id")
            + Suppress("=")
            + Group(OneOrMore(_descriptor_pe, stop_on=(LineEnd() ^ "{")))(
                "entity_descriptors"
            )
            + Optional(
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
)
