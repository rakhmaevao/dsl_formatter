from dsl_token import PreToken, Address
import re

class DslTokenizer:
    def tokenize(self, content: str, file_path: str) -> list[PreToken]:
        lines = content.split("\n")
        result = []
        for line_i, line in enumerate(lines):
            if line.lstrip().startswith('//') or line.lstrip().startswith('#'):
                result.append(
                    PreToken(
                        value=line.lstrip(),
                        address=Address(file_path=file_path, line=line_i + 1),
                    )
                )
                result.append(
                    PreToken(
                        value="\n",
                        address=Address(file_path=file_path, line=line_i + 1),
                    )
                )
                continue
            for token in self.__split_ignore_quotes(line):
                result.append(
                    PreToken(
                        value=token,
                        address=Address(file_path=file_path, line=line_i + 1),
                    )
                )
            result.append(
                    PreToken(
                        value="\n",
                        address=Address(file_path=file_path, line=line_i + 1),
                    )
                )
        return result

    @staticmethod
    def __split_ignore_quotes(input_string):
        pattern = r'(".*?"|\S+)'
        return re.findall(pattern, input_string)