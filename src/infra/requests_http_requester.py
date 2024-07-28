import requests

from src.application.interfaces.http_requester import HttpRequester


class RequestsHttpRequester(HttpRequester):
    @staticmethod
    def ping(url: str) -> bool:
        try:
            response = requests.get(url)
            if response.status_code in range(200, 300):
                return True
        except requests.RequestException:
            return False
        return False
