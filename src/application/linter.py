from pathlib import Path
from src.application.checkers.url_checker import UrlChecker
from src.domain.checkers import CheckResult
from src.domain.supported_file import DslFile, MdFile


class Linter:
    def __init__(self, checkers: list[UrlChecker]) -> None:
        self.__checkers = checkers

    def run(self, path: Path, verbose: bool) -> list[CheckResult]:
        check_results = []
        if path.is_dir():
            for file in path.iterdir():
                check_results += self.run(file, verbose)
        match path.suffix:
            case ".dsl":
                supported_file = DslFile(path=path, body=path.read_text())
            case ".md":
                supported_file = MdFile(path=path, body=path.read_text())
            case _:
                return check_results
        if verbose:
            print(f"Checking {path}")
        results_for_this_file = []
        for checker in self.__checkers:
            results_for_this_file += checker(supported_file)
        if results_for_this_file and verbose:
            print(f"Found {len(results_for_this_file)} problems in {path}")
        check_results += results_for_this_file
        return check_results
