from __future__ import annotations
from dataclasses import dataclass


@dataclass
class DslInstruction:
    id: str
    argument: str


@dataclass
class C4Node:
    id: str
    type: str
    name: str
    description: str | None
    technology: str | None
    children: list[C4Node | DslInstruction]


@dataclass
class C4Module:
    body: list[C4Node]
