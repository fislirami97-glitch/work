import re
from app.schemas import DiscoveredItem

PRICE_PATTERNS = [
    (re.compile(r"\$\s?(\d+(?:\.\d+)?)"), "USD"),
    (re.compile(r"(\d+(?:[\.,]\d+)?)\s?(?:DA|DZD)", re.I), "DZD"),
    (re.compile(r"£\s?(\d+(?:\.\d+)?)"), "GBP"),
    (re.compile(r"€\s?(\d+(?:\.\d+)?)"), "EUR"),
]

def enrich_from_text(item: DiscoveredItem) -> DiscoveredItem:
    text = f"{item.title} {item.snippet}"
    if item.price is None:
        for rx, currency in PRICE_PATTERNS:
            m = rx.search(text)
            if m:
                item.price = float(m.group(1).replace(",", "."))
                item.currency = currency
                break

    if item.sold_count is None:
        m = re.search(r"([\d,.]+)\s*(?:sold|orders?)", text, re.I)
        if m:
            try:
                item.sold_count = int(float(m.group(1).replace(",", "")))
            except Exception:
                pass

    if item.review_count is None:
        m = re.search(r"([\d,.]+)\s*(?:reviews?|ratings?)", text, re.I)
        if m:
            try:
                item.review_count = int(float(m.group(1).replace(",", "")))
            except Exception:
                pass

    if item.moq is None:
        m = re.search(r"MOQ\s*[:\-]?\s*(\d+)", text, re.I)
        if m:
            item.moq = int(m.group(1))
    return item
