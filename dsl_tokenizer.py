from dsl_token import Token, Address, Token
import re

class DslTokenizer:
    def pre_tokenize(self, content: str, file_path: str) -> list[Token]:
        lines = content.split("\n")
        result = []
        for line_i, line in enumerate(lines):
            if line.lstrip().startswith('//') or line.lstrip().startswith('#'):
                result.append(
                    Token(
                        value=line.lstrip(),
                        address=Address(file_path=file_path, line=line_i + 1),
                    )
                )
                result.append(
                    Token(
                        value="\n",
                        address=Address(file_path=file_path, line=line_i + 1),
                    )
                )
                continue
            for token in self.__split_ignore_quotes(line):
                result.append(
                    Token(
                        value=token,
                        address=Address(file_path=file_path, line=line_i + 1),
                    )
                )
            result.append(
                    Token(
                        value="\n",
                        address=Address(file_path=file_path, line=line_i + 1),
                    )
                )
        return result
    
    def define_types(self, pre_tokens: list[Token]) -> list[Token]:
        tokens = []
        # for i, pre_token in enumerate(pre_tokens):
        #     if pre_tokens[i + 1].value == "->":


    @staticmethod
    def __split_ignore_quotes(input_string):
        pattern = r'(".*?"|\S+)'
        return re.findall(pattern, input_string)