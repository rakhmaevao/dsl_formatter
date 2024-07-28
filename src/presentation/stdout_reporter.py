from src.domain.checkers import CheckResult


class StdoutReporter:
    def report(self, results: list[CheckResult]) -> None:
        print(f"Found {len(results)} problems:")
        for result in results:
            print(result)
