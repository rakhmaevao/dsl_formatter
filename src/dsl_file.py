from dataclasses import dataclass
from pathlib import Path


@dataclass
class DslFile:
    path: Path
    body: str
