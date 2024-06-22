from dataclasses import dataclass

@dataclass
class Node:
    pass

@dataclass
class C4Module:
    body: list[Node]

@dataclass
class C4Container(Node):
    id: str
    name: str
    description: str | None
    technology: str | None
    tags: list[str]
    children: list[Node]