from abc import ABC, abstractmethod

class MarketSource(ABC):
    name = "Base Source"
    source_type = "Unknown"

    @abstractmethod
    def fetch(self, ticker: str, limit: int = 10):
        pass