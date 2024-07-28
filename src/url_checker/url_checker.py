# URL-ы активные
# URL-ы без якоря


from dataclasses import dataclass
import re

from src.checkers import CheckProblemLevel, CheckResult, FullChecker
from src.dsl_file import DslFile
from src.interfaces.http_requester import HttpRequester


class UrlCheckResult(CheckResult):
    pass


class UrlIsNotActiveCheckResult(UrlCheckResult):
    _CODE = "U001"
    _DESCRIPTION = "URL is not active"
    _REASON = "URL must be active"
    _LEVEL = CheckProblemLevel.ERROR

    def __init__(self, url: str, file: DslFile, line_number: int) -> None:
        self._url = url
        super().__init__(file, line_number)


@dataclass(frozen=True, slots=True)
class UrlWithAddressInFile:
    url: str
    line_number: int
    file: DslFile


class UrlChecker(FullChecker):
    def __init__(self, http_requester: HttpRequester) -> None:
        self.__http_requester = http_requester

    def __call__(self, dsl_file: DslFile) -> list[UrlCheckResult]:
        urls: list[UrlWithAddressInFile] = []
        for i, line in enumerate(dsl_file.body.splitlines()):
            if re.match(r"^\s*url\s", line):
                url = line.split("url ")[1]
                urls.append(
                    UrlWithAddressInFile(url=url, line_number=i + 1, file=dsl_file)
                )
        check_results = []
        for url in urls:
            result = self.__check_active_url(url)
            if result is not None:
                check_results.append(result)
        return check_results

    def __check_active_url(
        self, url: UrlWithAddressInFile
    ) -> None | UrlIsNotActiveCheckResult:
        if self.__http_requester.ping(url.url):
            return None
        return UrlIsNotActiveCheckResult(url.url, url.file, url.line_number)
