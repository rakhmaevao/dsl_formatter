from pathlib import Path
from src.application.checkers.url_checker import UrlChecker
from src.application.linter import Linter
from src.domain.checkers import CheckResult
from src.infra.requests_http_requester import RequestsHttpRequester
from src.presentation.stdout_reporter import StdoutReporter


class App:
    def __init__(self) -> None:
        checkers = [
            UrlChecker(http_requester=RequestsHttpRequester()),
        ]
        self.__linter = Linter(checkers=checkers)
        self.__reporter = StdoutReporter()

    def run(self, path: Path, verbose: bool) -> list[CheckResult]:
        results = self.__linter.run(path, verbose)
        self.__reporter.report(results)
