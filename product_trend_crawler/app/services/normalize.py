import re

STOP = {
    "buy","shop","online","sale","price","amazon","alibaba","tiktok","wholesale",
    "best","new","official","2026","for","and","with","the","a","an"
}

def canonicalize_title(title: str) -> str:
    s = title.lower()
    s = re.sub(r"[^\w\s-]", " ", s, flags=re.UNICODE)
    words = [w for w in s.split() if w not in STOP and len(w) > 1]
    return " ".join(words[:12]).strip() or title.lower().strip()

def infer_source(domain: str) -> str:
    d = domain.lower()
    if "tiktok" in d: return "tiktok_shop"
    if "amazon" in d: return "amazon"
    if "alibaba" in d: return "alibaba"
    if "made-in-china" in d: return "made_in_china"
    if "ouedkniss" in d or ".dz" in d: return "algeria_market"
    return d
