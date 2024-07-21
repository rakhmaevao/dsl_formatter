from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


@dataclass(frozen=True)
class Address:
    file_path: str
    line: int


class Token:
    def __init__(self, value: str, address: Address) -> None:
        self.__value = value
        self.__address = address

    @property
    def value(self) -> str:
        return self.__value
    
    @property
    def address(self) -> Address:
        return self.__address

    def __eq__(self, other: Token) -> bool:
        return self.__value == other.value and self.__address == other.address


class TokenType(Enum):
    COMMENT = "comment"
    VARIABLE = "variable"
    EQUAL_OPERATOR = "equal_operator"
    NEW_LINE = "newline"
    DSL_KEYWORD = "dsl_keyword"
    ARROW = "arrow"
    
    DSL_CONNECTION_SRC = "dsl_connection_src"
    DSL_CONNECTION_DST = "dsl_connection_dst"
    
    DSL_DESCRIPTION = "dsl_description"
    DSL_TECHNOLOGY = "dsl_technology"
    DSL_TAGS = "dsl_tags"
