from abc import ABC, abstractmethod
from typing import Iterable
from app.schemas import DiscoveredItem

class Collector(ABC):
    @abstractmethod
    async def search(self, query: str, domain: str, limit: int = 10) -> Iterable[DiscoveredItem]:
        raise NotImplementedError
