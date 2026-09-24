def build_query(source: str, seed: str) -> str:
    if source == "tiktok_shop":
        return f'"{seed}" product sold reviews'
    if source == "amazon":
        return f'"{seed}" product reviews rating'
    if source in {"alibaba", "made_in_china"}:
        return f'"{seed}" product MOQ price'
    if source == "algeria_market":
        return f'"{seed}" prix DA'
    return f'"{seed}" product'
