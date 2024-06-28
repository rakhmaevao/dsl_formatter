from ..module import DslModule, DslNode, DslProperty
from pyparsing import (
    ParseResults,
)
from loguru import logger

from .parser_elements import c4_node_pe


class DslParser:
    def __call__(self, content: str) -> DslModule:
        pp_result = c4_node_pe.parse_string(content)
        logger.debug(f"PP parsing:\n{pp_result.dump()}")
        result = []
        for element in pp_result:
            result += self.__further_parse_one_layer(element)
        return DslModule(body=result)

    def __further_parse_one_layer(self, pp_result: ParseResults) -> list[DslNode]:
        logger.info(f"Parsing: {pp_result.as_dict()}")
        nodes = []
        children = []
        if "children" in pp_result:
            children = self.__parse_children(pp_result.get("children"))
        nodes.append(
            DslNode(
                id=pp_result["entity_id"],
                descriptors=pp_result["entity_descriptors"].as_list(),
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
