from __future__ import annotations
from dataclasses import dataclass


@dataclass
class Node:
    id: str
    name: str
    description: str | None
    technology: str | None
    tags: str
    children: list[Node]
    type: str = "unknown"

@dataclass
class C4Module:
    body: list[Node]


@dataclass
class C4Container(Node):
    type: str = "container"
