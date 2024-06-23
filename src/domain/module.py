from __future__ import annotations
from dataclasses import dataclass


@dataclass
class DslProperty:
    id: str
    argument: str


@dataclass
class DslNode:
    id: str
    type: str
    name: str
    description: str | None
    technology: str | None
    children: list[DslNode | DslProperty]


@dataclass
class DslModule:
    body: list[DslNode]
