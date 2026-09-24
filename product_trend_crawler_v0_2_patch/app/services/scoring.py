from collections import Counter
import math

def score_product(product):
    listings = product.listings
    by_source = Counter(l.source for l in listings)
    intl = [l for l in listings if l.source in {"tiktok_shop", "amazon"}]
    china = [l for l in listings if l.source in {"alibaba", "made_in_china", "1688"}]
    dz = [l for l in listings if l.source == "algeria_market"]

    max_sold = max((l.sold_count or 0 for l in intl), default=0)
    max_reviews = max((l.review_count or 0 for l in intl), default=0)
    sold_signal = min(1.0, math.log10(max_sold + 1) / 4.0)
    review_signal = min(1.0, math.log10(max_reviews + 1) / 4.0)
    social = 1.0 if any(l.source == "tiktok_shop" for l in intl) else 0.0
    amazon = 1.0 if any(l.source == "amazon" for l in intl) else 0.0
    trend = 25 * min(1.0, .45*sold_signal + .30*review_signal + .15*social + .10*amazon)

    demand = max(sold_signal, review_signal, 0.35 if intl else 0.0)
    gap = 25 * demand * (1 - min(1.0, len(dz)/6.0))

    prices = [l.price for l in china if l.price is not None and l.currency in {None, "USD"}]
    best = min(prices) if prices else None
    profit = 5 if best is None else 20 if best <= 1 else 17 if best <= 3 else 13 if best <= 6 else 8 if best <= 12 else 4

    title = product.canonical_name.lower()
    demo = {"lock","guard","protector","childproof","babyproof","stopper","alarm","sensor","anti-tip","restrictor","shield","cover"}
    creative = min(15, 5 + sum(1.7 for x in demo if x in title))

    sourcing = 0
    if china:
        sourcing += 4
        moqs = [l.moq for l in china if l.moq is not None]
        if moqs and min(moqs) <= 100: sourcing += 3
        if len(china) >= 2: sourcing += 3

    bulky = any(x in title for x in {"gate","bed rail","crib","chair","stroller"})
    shipping = 2 if bulky else 5
    total = round(min(100, trend + gap + profit + creative + sourcing + shipping), 1)

    metric_count = sum(1 for l in listings if any(v is not None for v in [l.price,l.sold_count,l.review_count,l.moq]))
    confidence = round(min(100, len(by_source)*18 + min(46, metric_count*10)), 1)

    if len(dz) >= 5: status = "SATURATED"
    elif total >= 78 and confidence >= 45 and len(dz) <= 2: status = "BREAKOUT"
    elif total >= 65 and confidence >= 30 and len(dz) <= 2: status = "EARLY"
    elif total >= 52: status = "WATCH"
    else: status = "WEAK"
    return total, confidence, status
