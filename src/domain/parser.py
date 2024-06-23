from dataclasses import dataclass
from .module import C4Module, C4Node, DslInstruction
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
_c4_node_pe = Forward()

_c4_node_pe << (
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
            (_property_pe ^ _c4_node_pe),
            ignore_expr=(c_style_comment),
        )
    )("children")
)


@dataclass
class _Property:
    id: str
    argument: str


class DslParser:
    def __call__(self, content: str) -> C4Module:
        raw_parsing = _c4_node_pe.parse_string(content)
        logger.info(f"Parsing {raw_parsing.as_list()}")
        return C4Module(body=self.__further_parse_one_layer(raw_parsing))

    def __further_parse_one_layer(self, raw_parsing: ParseResults) -> list[C4Node]:
        logger.debug(f"Parsing one layer {raw_parsing}")
        nodes = []
        children = []
        if "children" in raw_parsing:
            logger.debug(f"Fined children for `{raw_parsing.get("entity_id")}`")
            children = self.__parse_children(raw_parsing.get("children"))
        logger.debug(f"End of parsing {raw_parsing}. Start create C4Node")
        nodes.append(
            C4Node(
                id=raw_parsing["entity_id"],
                type=raw_parsing["entity_type"],
                name=raw_parsing["entity_name"],
                description=None,
                technology=None,
                children=[
                    DslInstruction(id=child.id, argument=child.argument)
                    if isinstance(child, _Property)
                    else child
                    for child in children
                ],
            )
        )
        return nodes

    def __parse_children(self, raw_children: ParseResults) -> list[_Property | C4Node]:
        logger.debug(f"Parsing children {raw_children}")
        children = []
        child_part = raw_children[0]
        for child in child_part:
            if len(child) == 2:
                children.append(
                    _Property(
                        id=child[0],
                        argument=child[1],
                    )
                )
        if "entity_id" in child_part:
            children += self.__further_parse_one_layer(child_part)
        return children
