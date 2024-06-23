from __future__ import annotations
from dataclasses import dataclass


@dataclass
class DslInstruction:
    id: str
    argument: str


@dataclass
class C4Node:
    id: str
    name: str
    description: str | None
    technology: str | None
    tags: str
    children: list[C4Node | DslInstruction]
    type: str = "unknown"


@dataclass
class C4Module:
    body: list[C4Node]


@dataclass
class C4Container(C4Node):
    type: str = "container"

@dataclass
class C4Component(C4Node):
    type: str = "component"