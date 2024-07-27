from abc import ABC, abstractmethod


class Parser(ABC):
    @abstractmethod
    def parse_page(self, url):
        pass

    @abstractmethod
    def parse_pages(self):
        pass
