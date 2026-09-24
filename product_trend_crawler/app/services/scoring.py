from collections import Counter
from sqlalchemy.orm import Session
from app.models import Product

def clamp(v, lo=0, hi=100):
    return max(lo, min(hi, v))

def score_product(product: Product) -> tuple[float, str, dict]:
    listings = product.listings
    sources = Counter(l.source for l in listings)

    intl = [l for l in listings if l.source in {"tiktok_shop","amazon"}]
    china = [l for l in listings if l.source in {"alibaba","made_in_china","1688"}]
    dz = [l for l in listings if l.source == "algeria_market"]

    sold = max([l.sold_count or 0 for l in intl], default=0)
    reviews = max([l.review_count or 0 for l in intl], default=0)

    # Trend proxy for MVP; daily snapshot velocity will replace this.
    trend = clamp((sold / 1000) * 10 + (reviews / 500) * 8)
    trend = trend / 100 * 25

    # Fewer Algerian listings => larger gap.
    gap_raw = 100 if len(dz) == 0 else max(0, 100 - len(dz) * 18)
    algeria_gap = gap_raw / 100 * 25

    # Simple cost heuristic from China listings.
    china_prices = [l.price for l in china if l.price and (l.currency == "USD" or l.currency is None)]
    best_cost = min(china_prices) if china_prices else None
    if best_cost is None:
        profit = 8
    elif best_cost <= 1:
        profit = 20
    elif best_cost <= 3:
        profit = 17
    elif best_cost <= 6:
        profit = 14
    elif best_cost <= 12:
        profit = 9
    else:
        profit = 5

    title = product.canonical_name.lower()
    demo_words = {"lock","guard","protector","safety","anti","childproof","babyproof","stopper","alarm","sensor"}
    creative = min(15, 4 + sum(2 for w in demo_words if w in title))

    sourcing = 0
    if china:
        sourcing += 5
        moqs = [l.moq for l in china if l.moq is not None]
        if moqs and min(moqs) <= 100:
            sourcing += 3
        if len(china) >= 2:
            sourcing += 2

    # MVP assumes small baby-safety accessories unless keywords imply bulky products.
    bulky = any(x in title for x in {"gate","bed rail","crib","chair","stroller"})
    shipping = 2 if bulky else 5

    total = round(trend + algeria_gap + profit + creative + sourcing + shipping, 1)

    if total >= 85 and len(dz) <= 1:
        status = "BREAKOUT"
    elif total >= 75 and len(dz) <= 2:
        status = "EARLY"
    elif total >= 65:
        status = "VALIDATED"
    else:
        status = "SATURATED_OR_WEAK"

    parts = {
        "trend": round(trend,1),
        "algeria_gap": round(algeria_gap,1),
        "profit": round(profit,1),
        "creative": round(creative,1),
        "sourcing": round(sourcing,1),
        "shipping": round(shipping,1),
    }
    return total, status, parts
