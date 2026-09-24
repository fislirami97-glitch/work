import httpx
from app.collectors.base import Collector
from app.schemas import DiscoveredItem
from app.settings import settings

class SerperCollector(Collector):
    endpoint = "https://google.serper.dev/search"

    async def search(self, query: str, domain: str, limit: int = 10):
        if not settings.serper_api_key:
            return []
        q = f"site:{domain} {query}"
        headers = {
            "X-API-KEY": settings.serper_api_key,
            "Content-Type": "application/json",
            "User-Agent": settings.user_agent,
        }
        payload = {"q": q, "num": min(limit, 10), "gl": "us", "hl": "en"}
        async with httpx.AsyncClient(timeout=settings.request_timeout) as client:
            r = await client.post(self.endpoint, headers=headers, json=payload)
            r.raise_for_status()
            data = r.json()
        return [DiscoveredItem(source=domain, title=x.get("title", "") or "", url=x.get("link", "") or "", snippet=x.get("snippet", "") or "") for x in data.get("organic", [])]
