from abc import ABC
from enum import Enum
from src.domain.dsl_file import DslFile


class CheckProblemLevel(Enum):
    ERROR = "ERROR"
    WARNING = "WARNING"


class CheckResult:
    _CODE = "UNKNOWN"
    _REASON = "Unknown reason"
    _LEVEL = CheckProblemLevel.ERROR

    def __init__(self, file: DslFile, line_number: int) -> None:
        self._file = file
        self._line_number = line_number

    def __repr__(self) -> str:
        return f"{self._file.path}:{self._line_number}: {self._LEVEL.value} {self._CODE}: {self._REASON}"


class FullChecker(ABC):
    def __call__(self, dsl_file: DslFile) -> None:
        raise NotImplementedError
