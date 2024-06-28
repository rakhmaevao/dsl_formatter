from ..module import DslModule, DslNode, DslProperty
from pyparsing import (
    ParseResults,
)
from loguru import logger

from .parser_elements import c4_node_pe


class DslParser:
    def __call__(self, content: str) -> DslModule:
        raw_parsing = c4_node_pe.parse_string(content)
        logger.debug(f"Raw parsing:\n{raw_parsing.dump()}")
        return DslModule(body=self.__further_parse_one_layer(raw_parsing))

    def __further_parse_one_layer(self, raw_parsing: ParseResults) -> list[DslNode]:
        nodes = []
        children = []
        if "children" in raw_parsing:
            children = self.__parse_children(raw_parsing.get("children"))
        nodes.append(
            DslNode(
                id=raw_parsing["entity_id"],
                descriptors=raw_parsing["entity_descriptors"].as_list(),
                children=children,
            )
        )
        return nodes

    def __parse_children(
        self, raw_children: ParseResults
    ) -> list[DslProperty | DslNode]:
        child_part = raw_children[0]
        st_children = " ".join(child_part)
        logger.info(f"Children: {child_part[0]}")
        children = []

        for child in child_part:
            if isinstance(child, ParseResults):
                if child.get_name() == "property":
                    children.append(
                        DslProperty(
                            id=child[0],
                            argument=child[1],
                        )
                    )
        if "entity_id" in child_part:
            children += self.__further_parse_one_layer(child_part)
        return children
