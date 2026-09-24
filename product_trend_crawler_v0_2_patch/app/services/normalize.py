import re

NOISE = {
    "buy","shop","online","sale","price","amazon","alibaba","tiktok","wholesale",
    "best","new","official","for","and","with","the","pack","pcs","piece",
    "manufacturer","supplier","factory","custom","oem","odm","china","free","shipping"
}

def tokens(text: str):
    s = text.lower()
    s = re.sub(r"\([^)]*\)", " ", s)
    s = re.sub(r"\[[^\]]*\]", " ", s)
    s = re.sub(r"\b\d+(?:\.\d+)?\b", " ", s)
    s = re.sub(r"[^\w\s-]", " ", s, flags=re.UNICODE)
    return [w for w in s.split() if w not in NOISE and len(w) > 2]

def canonicalize_title(title: str) -> str:
    ws = tokens(title)
    return " ".join(ws[:10]).strip() or title.lower().strip()

def similarity(a: str, b: str) -> float:
    aa, bb = set(tokens(a)), set(tokens(b))
    if not aa or not bb:
        return 0.0
    inter = aa & bb
    if len(inter) < 2:
        return 0.0
    return len(inter) / len(aa | bb)
