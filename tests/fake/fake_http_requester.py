from src.interfaces.http_requester import HttpRequester


class FakeHttpRequester(HttpRequester):
    def ping(self, url: str) -> bool:
        if url in ("https://good.com", "https://other.com"):
            return True
        return False
