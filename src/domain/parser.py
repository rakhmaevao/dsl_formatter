from .module import C4Container, C4Module, DslInstruction
from pyparsing import (
    Combine,
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

_children_pe = nested_expr("{", "}", ignore_expr=(quoted_string | c_style_comment))

_full_entity_description_pe = (
    _entity_id_pe
    + Suppress("=")
    + _entity_type_pe
    + Suppress('"')
    + _entity_name_pe
    + Suppress('"')
    + _children_pe
)


class DslParser:
    _ENTITY_ID_INDEX = 0
    _ENTITY_TYPE_INDEX = 1
    _ENTITY_NAME_INDEX = 2
    _ENTITY_CHILDREN_INDEX = 3

    def __call__(self, content: str) -> C4Module:
        module = C4Module(body=[])
        raw_parsing = _full_entity_description_pe.parseString(content).asList()
        entity_id = raw_parsing[self._ENTITY_ID_INDEX]
        entity_type = raw_parsing[self._ENTITY_TYPE_INDEX]
        entity_name = raw_parsing[self._ENTITY_NAME_INDEX]
        logger.debug(f"{raw_parsing=}")
        tags = ""
        children_raw = raw_parsing[self._ENTITY_CHILDREN_INDEX]
        children = []
        skip_next = False
        for i, child_part in enumerate(children_raw):
            if skip_next:
                skip_next = False
                continue
            if child_part == "tags":
                tags = self.__parse_tags(children_raw[i + 1])
                skip_next = True
            elif child_part.startswith("!"):
                children.append(
                    DslInstruction(id=child_part, argument=children_raw[i + 1])
                )
                skip_next = True

        match entity_type:
            case "container":
                module.body.append(
                    C4Container(
                        id=entity_id,
                        name=entity_name,
                        description=None,
                        technology=None,
                        tags=tags,
                        children=children,
                    )
                )
            case _:
                raise NotImplementedError(f"Unsupported entity type: {entity_type}")

        return module

    def __parse_tags(self, raw_tags: str) -> str:
        return raw_tags[1:-1].replace(" ", "").split(",")
