from src.domain.module import C4Module


class CodeGenerator:
    def __call__(self, module: C4Module) -> str:
        result = ""
        for element in module.body:
            new_line = f'{element.id} = {element.type} \"{element.name}\" {{\n    tags "{element.tags}"\n}}'
            result += new_line
        return result