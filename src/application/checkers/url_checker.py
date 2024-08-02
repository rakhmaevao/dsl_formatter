from dataclasses import dataclass
import re

from loguru import logger

from src.domain.checkers import CheckProblemLevel, CheckResult, FullChecker
from src.domain.supported_file import DslFile, MdFile, SupportedFile
from src.application.interfaces.http_requester import HttpRequester


class UrlCheckResult(CheckResult):
    pass


class UrlIsNotActiveCheckResult(UrlCheckResult):
    _CODE = "U001"
    _DESCRIPTION = "URL is not active"
    _REASON = "URL must be active"
    _LEVEL = CheckProblemLevel.ERROR

    def __init__(self, url: str, file: SupportedFile, line_number: int) -> None:
        self._url = url
        super().__init__(file, line_number)


@dataclass(frozen=True, slots=True)
class UrlWithAddressInFile:
    url: str
    line_number: int
    file: SupportedFile


class UrlChecker(FullChecker):
    def __init__(self, http_requester: HttpRequester) -> None:
        self.__http_requester = http_requester

    def __call__(self, file: SupportedFile) -> list[UrlCheckResult]:
        urls = self.__collect_urls(file)

        check_results = []
        for url in urls:
            result = self.__check_active_url(url)
            if result is not None:
                check_results.append(result)
        return check_results

    def __collect_urls(self, file: SupportedFile) -> list[UrlWithAddressInFile]:
        urls: list[UrlWithAddressInFile] = []
        if isinstance(file, DslFile):
            for i, line in enumerate(file.body.splitlines()):
                if re.match(r"^\s*url\s", line):
                    url = line.split("url ")[1]
                    urls.append(
                        UrlWithAddressInFile(url=url, line_number=i + 1, file=file)
                    )
        if isinstance(file, MdFile):
            for i, line in enumerate(file.body.splitlines()):
                urls += [
                    UrlWithAddressInFile(url=matching[1], line_number=i + 1, file=file)
                    for matching in re.findall(
                        r"\[(.*?)\]\((https?://[^\s()]+)\)", line
                    )
                ]
        return urls

    def __check_active_url(
        self, url: UrlWithAddressInFile
    ) -> None | UrlIsNotActiveCheckResult:
        logger.info(f"Checking {url.url} {self.__http_requester.ping(url.url)}")
        if self.__http_requester.ping(url.url):
            return None
        return UrlIsNotActiveCheckResult(url.url, url.file, url.line_number)
