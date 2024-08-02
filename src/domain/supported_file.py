from abc import ABC
from dataclasses import dataclass
from pathlib import Path


@dataclass
class SupportedFile(ABC):
    path: Path
    body: str


class DslFile(SupportedFile):
    pass


class MdFile(SupportedFile):
    pass
