from abc import ABC, abstractmethod


class HttpRequester(ABC):
    @staticmethod
    @abstractmethod
    def ping(url: str) -> bool:
        raise NotImplementedError
