from .module import C4Component, C4Container, C4Module, C4Node, DslInstruction
from pyparsing import (
    Combine,
    Forward,
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
    quoted_string,
)
from loguru import logger

_entity_id_pe = Word(alphas + "_")
_entity_type_pe = Word(alphas + "_")
_entity_name_pe = Word(alphas + "_")

_tags_pe = (
    Suppress("tags")
    + Suppress('"')
    + Word(alphas + nums + "_" + "," + " ")
    + Suppress('"')
)("tags")
_instruction_pe = (Combine(Word(alphas)) + Word(alphas))("instruction")

# _full_entity_description_pe = (
#     _entity_id_pe
#     + Suppress("=")
#     + _entity_type_pe
#     + Suppress('"')
#     + _entity_name_pe
#     + Suppress('"')
#     + _children_pe
# )

_c4_node_pe = Forward()

_c4_node_pe << (
    _entity_id_pe("entity_id")
    + Suppress("=")
    + _entity_type_pe("entity_type")
    + Suppress('"')
    + _entity_name_pe("entity_name")
    + Suppress('"')
    + Optional(
        nested_expr("{", "}", (_tags_pe ^ _c4_node_pe), ignore_expr=(c_style_comment))
    )("children")
)


class DslParser:
    def __call__(self, content: str) -> C4Module:
        raw_parsing = _c4_node_pe.parse_string(content).as_dict()
        logger.info(f"Parsing {raw_parsing["entity_id"]}")
        return C4Module(body=self.__further_parse_one_layer(raw_parsing))

    def __further_parse_one_layer(self, raw_parsing: dict) -> list[C4Node]:
        logger.debug(f"Parsing one layer {raw_parsing}")
        nodes = []
        tags, children = [], []
        if "children" in raw_parsing:
            logger.debug(f"Fined children for `{raw_parsing["entity_id"]}`")
            tags, children = self.__parse_children(raw_parsing["children"])
        logger.debug(f"End of parsing {raw_parsing}. Start create C4Node")
        match raw_parsing["entity_type"]:
            case "container":
                nodes.append(
                    C4Container(
                        id=raw_parsing["entity_id"],
                        name=raw_parsing["entity_name"],
                        description=None,
                        technology=None,
                        tags=tags,
                        children=children,
                    )
                )
            case "component":
                nodes.append(
                    C4Component(
                        id=raw_parsing["entity_id"],
                        name=raw_parsing["entity_name"],
                        description=None,
                        technology=None,
                        tags=tags,
                        children=children,
                    )
                )
            case _:
                raise NotImplementedError(
                    f"Unsupported entity type: {raw_parsing['entity_type']}"
                )
        return nodes

    def __parse_tags(self, raw_tags: str) -> str:
        return raw_tags.replace(" ", "").split(",")

    def __parse_children(self, raw_children: list[dict]) -> tuple[str, list]:
        logger.debug(f"Parsing children {raw_children}")
        tags = []
        children = []
        skip_next = False
        for i, child_part in enumerate(raw_children):
            logger.debug(f"Parsing child {child_part}")
            if isinstance(child_part, dict):
                children += self.__further_parse_one_layer(child_part)
                continue
            if skip_next:
                skip_next = False
                continue
            if "tags" in child_part:
                tags = self.__parse_tags(child_part["tags"][0])
            elif child_part.startswith("!"):
                children.append(
                    DslInstruction(id=child_part, argument=raw_children[i + 1])
                )
                skip_next = True
        return tags, children
