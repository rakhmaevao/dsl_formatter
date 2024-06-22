from .tree.module import C4Container, C4Module
from pyparsing import Word, ZeroOrMore, alphas, Suppress

_entity_id_pe = Word(alphas + '_')
_entity_type_pe = Word(alphas + '_')
_entity_name_pe = Word(alphas + '_')
_full_entity_description_pe = _entity_id_pe + ZeroOrMore(" ") +  Suppress("=") + ZeroOrMore(" ") + _entity_type_pe + Suppress('"') + _entity_name_pe + Suppress('"')

class DslParser:
    def __call__(self, content: str) -> C4Module:
        module = C4Module(body=[])
        raw_parsing = _full_entity_description_pe.parseString(content)
        entity_id = raw_parsing[0]
        entity_type = raw_parsing[1]
        entity_name = raw_parsing[2]
        match entity_type:
            case "container":
                module.body.append(C4Container(id=entity_id, name=entity_name, description=None, technology=None, tags=[], children=[]))
            case _:
                raise NotImplementedError(f"Unsupported entity type: {entity_type}")

        return module