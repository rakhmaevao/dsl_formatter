from pathlib import Path
from src.application.checkers.url_checker import UrlChecker
from src.domain.checkers import CheckResult
from src.domain.dsl_file import DslFile


class Linter:
    def __init__(self, checkers: list[UrlChecker]) -> None:
        self.__checkers = checkers

    def run(self, path: Path) -> list[CheckResult]:
        check_results = []
        if path.is_dir():
            for file in path.iterdir():
                self.run(file)
        else:
            dsl_file = DslFile(path=path, body=path.read_text())
            for checker in self.__checkers:
                check_results += checker(dsl_file)
            # TODO(rao): Тут бы этап фильтрации сделать
        return check_results
