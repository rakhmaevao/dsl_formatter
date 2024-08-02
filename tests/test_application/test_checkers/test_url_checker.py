from pathlib import Path
import pytest
from src.domain.supported_file import DslFile, MdFile
from src.application.checkers.url_checker import UrlChecker
from tests.fake.fake_http_requester import FakeHttpRequester


@pytest.mark.parametrize(
    "dsl_file, expected",
    [
        (
            DslFile(
                path=Path("test_file.dsl"),
                body="""
                blocks = container "blocks" {
                    !docs docs
                    tags "middleware"
                    # domain layer
                    mask_processor = component "Mask Processor" {
                        url https://good.com
                        tags "domain_layer"
                    }

                    # service layer
                    user_library_services = component "user library services" {
                        url https://other.com
                        tags "service_layer"
                    }
                    GetNestedBlockLayoutService = component "GetNestedBlockLayoutService" {
                        url https://bad.com
                        tags "service_layer"
                    }

                }
                """,
            ),
            ["test_file.dsl:17: ERROR U001: URL must be active"],
        ),
        (
            MdFile(
                path=Path("test_file.md"),
                body="""
                Some test from markdown docs

                [Some label](https://good.com)

                Some text with [url](https://bad.com)
                """,
            ),
            ["test_file.md:4: ERROR U001: URL must be active"],
        ),
    ],
)
def test_url_checker(dsl_file, expected) -> None:
    url_checker = UrlChecker(http_requester=FakeHttpRequester())

    assert [str(r) for r in url_checker(dsl_file)] == expected
