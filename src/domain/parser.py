from .module import C4Container, C4Module, C4Node, DslInstruction
from pyparsing import (
    Combine,
    Forward,
    White,
    Word,
    ZeroOrMore,
    alphas,
    Suppress,
    Optional,
    c_style_comment,
    nested_expr,
    quoted_string,
)
from loguru import logger

_entity_id_pe = Word(alphas + "_")
_entity_type_pe = Word(alphas + "_")
_entity_name_pe = Word(alphas + "_")

_tags_pe = "tags" + Suppress('"') + Word(alphas + "_" + ",") + Suppress('"')
_instruction_pe = Combine("!" + Word(alphas)) + Word(alphas)

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
    + Optional(nested_expr("{", "}", (_c4_node_pe), ignore_expr=(quoted_string | c_style_comment)))("children")
)


class DslParser:
    def __call__(self, content: str) -> C4Module:
        raw_parsing = _c4_node_pe.parse_string(content).as_dict()
        logger.info(f"Parsing {raw_parsing["entity_id"]}")
        return C4Module(body=self.__further_parse_one_layer(raw_parsing))

    def __further_parse_one_layer(self, raw_parsing: dict) -> list[C4Node]:
        logger.debug(f"Parsing one layer {raw_parsing}")
        nodes = []
        tags, children =  "", []
        if "children" in raw_parsing:
            logger.debug(f"Fined children for `{raw_parsing["entity_id"]}`")
            tags, children =  self.__parse_children(raw_parsing["children"])
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
            case _:
                raise NotImplementedError(f"Unsupported entity type: {raw_parsing['entity_type']}")
        return nodes
    
    def __parse_tags(self, raw_tags: str) -> str:
        return raw_tags[1:-1].replace(" ", "").split(",")

    def __parse_children(self, raw_children: dict) -> tuple[str, list]:
        logger.debug(f"Parsing children {raw_children}")
        tags = ""
        children = []
        skip_next = False
        for i, child_part in enumerate(raw_children):
            logger.debug(f"Parsing child {child_part}")
            if isinstance(child_part, list):
                children += self.__further_parse_one_layer(child_part)
                continue
            if skip_next:
                skip_next = False
                continue
            if child_part == "tags":
                tags = self.__parse_tags(raw_children[i + 1])
                skip_next = True
            elif child_part.startswith("!"):
                children.append(
                    DslInstruction(id=child_part, argument=raw_children[i + 1])
                )
                skip_next = True
        return tags, children