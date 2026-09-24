from pydantic import BaseModel, HttpUrl
from typing import Optional

class DiscoveredItem(BaseModel):
    source: str
    title: str
    url: str
    snippet: str = ""
    price: Optional[float] = None
    currency: Optional[str] = None
    sold_count: Optional[int] = None
    review_count: Optional[int] = None
    rating: Optional[float] = None
    moq: Optional[int] = None

class ProductOut(BaseModel):
    id: int
    canonical_name: str
    niche: str
    status: str
    score: float
    model_config = {"from_attributes": True}
