from pathlib import Path
from src.application.checkers.url_checker import UrlChecker
from src.domain.checkers import CheckResult
from src.domain.dsl_file import DslFile


class Linter:
    def __init__(self, checkers: list[UrlChecker]) -> None:
        self.__checkers = checkers

    def run(self, path: Path, verbose: bool) -> list[CheckResult]:
        check_results = []
        if path.is_dir():
            for file in path.iterdir():
                check_results += self.run(file, verbose)
        elif path.suffix != ".dsl":
            return []
        else:
            dsl_file = DslFile(path=path, body=path.read_text())
            if verbose:
                print(f"Checking {path}")
            results_for_this_file = []
            for checker in self.__checkers:
                results_for_this_file += checker(dsl_file)
            if results_for_this_file and verbose:
                print(f"Found {len(results_for_this_file)} problems in {path}")
            check_results += results_for_this_file
        return check_results
