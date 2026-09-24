import re
from app.schemas import DiscoveredItem

def compact_number(raw: str):
    raw = raw.strip().lower().replace(",", "")
    mult = 1
    if raw.endswith("k"):
        mult, raw = 1000, raw[:-1]
    elif raw.endswith("m"):
        mult, raw = 1_000_000, raw[:-1]
    try:
        return int(float(raw) * mult)
    except Exception:
        return None

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
                try:
                    item.price = float(m.group(1).replace(",", ".")); item.currency = currency; break
                except Exception:
                    pass
    if item.sold_count is None:
        m = re.search(r"(\d+(?:[\.,]\d+)?[kKmM]?)\s*(?:sold|sales|orders?)\b", text, re.I)
        if m: item.sold_count = compact_number(m.group(1))
    if item.review_count is None:
        m = re.search(r"(\d+(?:[\.,]\d+)?[kKmM]?)\s*(?:reviews?|ratings?)\b", text, re.I)
        if m: item.review_count = compact_number(m.group(1))
    if item.rating is None:
        m = re.search(r"\b([1-5](?:\.\d+)?)\s*(?:out of 5|stars?)\b", text, re.I)
        if m:
            try: item.rating = float(m.group(1))
            except Exception: pass
    if item.moq is None:
        m = re.search(r"\bMOQ\s*[:\-]?\s*(\d+)", text, re.I)
        if m: item.moq = int(m.group(1))
    return item
