from pathlib import Path
from src.application.checkers.url_checker import UrlChecker
from src.application.linter import Linter
from src.domain.checkers import CheckResult
from src.domain.dsl_file import DslFile
from src.infra.requests_http_requester import RequestsHttpRequester


# TODO(rao): Click  воткнуть!
class App:
    def __init__(self) -> None:
        checkers = [
            UrlChecker(http_requester=RequestsHttpRequester()),
        ]
        self.__linter = Linter(checkers=checkers)

    def run(self, path: Path) -> list[CheckResult]:
        results = self.__linter.run(path)
