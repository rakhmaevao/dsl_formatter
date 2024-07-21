
from dataclasses import dataclass


@dataclass(frozen=True)
class Address:
    file_path: str
    line: int


@dataclass(frozen=True)
class Token:
    value: str
    address: Address