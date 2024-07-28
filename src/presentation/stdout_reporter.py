from src.domain.checkers import CheckResult


class StdoutReporter:
    def report(self, results: list[CheckResult]) -> None:
        for result in results:
            print(result)
