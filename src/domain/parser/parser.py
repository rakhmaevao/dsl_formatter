from ..module import DslModule, DslNode, DslProperty
from pyparsing import (
    ParseResults,
)
from loguru import logger

from .parser_elements import c4_node_pe


class DslParser:
    def __call__(self, content: str) -> DslModule:
        raw_parsing = c4_node_pe.parse_string(content)
        logger.info(f"Parsing {raw_parsing.as_list()}")
        return DslModule(body=self.__further_parse_one_layer(raw_parsing))

    def __further_parse_one_layer(self, raw_parsing: ParseResults) -> list[DslNode]:
        logger.debug(f"Parsing one layer {raw_parsing}")
        nodes = []
        children = []
        if "children" in raw_parsing:
            logger.debug(f"Fined children for `{raw_parsing.get("entity_id")}`")
            children = self.__parse_children(raw_parsing.get("children"))
        logger.debug(f"End of parsing {raw_parsing}. Start create node")
        nodes.append(
            DslNode(
                id=raw_parsing["entity_id"],
                type=raw_parsing["entity_type"],
                name=raw_parsing["entity_name"],
                description=None,
                technology=None,
                children=children,
            )
        )
        return nodes

    def __parse_children(
        self, raw_children: ParseResults
    ) -> list[DslProperty | DslNode]:
        logger.debug(f"Parsing children {raw_children}")
        children = []
        child_part = raw_children[0]
        for child in child_part:
            if len(child) == 2:
                children.append(
                    DslProperty(
                        id=child[0],
                        argument=child[1],
                    )
                )
        if "entity_id" in child_part:
            children += self.__further_parse_one_layer(child_part)
        return children
