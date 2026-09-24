from urllib.parse import urlparse
import re

REJECT_TITLE_TERMS = {
    "factory directory", "manufacturers", "manufacturer", "suppliers",
    "supplier", "wholesale", "category", "catalog", "999.com",
    "best sellers", "search results", "home page"
}

def looks_like_product_page(source: str, url: str, title: str) -> bool:
    if not url or not title or len(title.strip()) < 8:
        return False
    low_title = title.lower()
    if any(term in low_title for term in REJECT_TITLE_TERMS):
        return False
    path = urlparse(url).path.lower()
    if source == "tiktok_shop":
        return any(x in path for x in ["/pdp/", "/product/", "/view/product/"])
    if source == "amazon":
        return "/dp/" in path or "/gp/product/" in path
    if source == "alibaba":
        return "/product-detail/" in path
    if source == "made_in_china":
        return "/product/" in path or re.search(r"/[a-z0-9-]+_[a-z0-9]+\.html$", path) is not None
    if source == "algeria_market":
        return any(x in path for x in ["/annonce/", "/product/", "/produit/"]) or path.endswith(".html")
    return True
