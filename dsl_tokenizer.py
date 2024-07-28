from dsl_token import Token, Address, Token, TokenType
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
    
    def define_types(self, tokens: list[Token]) -> list[Token]:
        for i in range(len(tokens)):
            try:
                if tokens[i + 1].value == "->":
                    tokens[i].define_type(TokenType.DSL_CONNECTION_SRC)
                    tokens[i + 1].define_type(TokenType.DSL_OPERATOR_ARROW)
                    tokens[i + 2].define_type(TokenType.DSL_CONNECTION_DST)
                    tokens[i + 3].define_type(TokenType.DSL_DESCRIPTION)
                    tokens[i + 4].define_type(TokenType.DSL_TECHNOLOGY)
                    tokens[i + 5].define_type(TokenType.DSL_TAGS)
            except IndexError:
                pass
        return tokens

    @staticmethod
    def __split_ignore_quotes(input_string):
        pattern = r'(".*?"|\S+)'
        return re.findall(pattern, input_string)