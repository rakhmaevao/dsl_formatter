from .module import C4Container, C4Module, DslInstruction
from pyparsing import Combine, Word, ZeroOrMore, alphas, Suppress, Optional
from loguru import logger

_entity_id_pe = Word(alphas + "_")
_entity_type_pe = Word(alphas + "_")
_entity_name_pe = Word(alphas + "_")

_tags_pe = "tags" + Suppress('"') + Word(alphas + "_" + ",") + Suppress('"')
_instruction_pe = Combine("!" + Word(alphas)) + Word(alphas)
_children_pe = Optional(_tags_pe) & Optional(_instruction_pe)

_full_entity_description_pe = (
    _entity_id_pe
    + Suppress("=")
    + _entity_type_pe
    + Suppress('"')
    + _entity_name_pe
    + Suppress('"')
    + Suppress("{")
    + _children_pe
    + Suppress("}")
)


class DslParser:
    def __call__(self, content: str) -> C4Module:
        module = C4Module(body=[])
        raw_parsing = _full_entity_description_pe.parseString(content).asList()
        entity_id = raw_parsing[0]
        entity_type = raw_parsing[1]
        entity_name = raw_parsing[2]
        logger.debug(f"{raw_parsing=}")
        tags = ""
        children = []
        skip_next = False
        for i, child_part in enumerate(raw_parsing[3:]):
            if skip_next:
                skip_next = False
                continue
            if child_part == "tags":
                tags = raw_parsing[3 + i + 1]
                skip_next = True
            elif child_part.startswith("!"):
                children.append(
                    DslInstruction(id=child_part, argument=raw_parsing[3 + i + 1])
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
                        tags=[tags],
                        children=children,
                    )
                )
            case _:
                raise NotImplementedError(f"Unsupported entity type: {entity_type}")

        return module
