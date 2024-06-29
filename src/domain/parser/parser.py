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
        if pp_result.get_name() == "property":
            return [
                DslProperty(
                    id=pp_result["property_name"], argument=pp_result["property_value"]
                )
            ]
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
        self, raw_str_children: ParseResults
    ) -> list[DslProperty | DslNode]:
        logger.info(f"Children: {raw_str_children}")
        raw_str_children = self.__rebuild_str_children(raw_str_children)
        pp_result = c4_node_pe.parse_string(raw_str_children)
        result = []
        for element in pp_result:
            result += self.__further_parse_one_layer(element)
        return result

    def __rebuild_str_children(self, raw_children: ParseResults) -> str:
        raw_children = raw_children[0]
        result = ""
        for child in raw_children.as_list():
            if isinstance(child, str):
                result += child
            if isinstance(child, list):
                result += "{" + "\n".join(child) + "}"
        return result
