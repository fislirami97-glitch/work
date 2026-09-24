from app.models import Product, Listing
from app.services.scoring import score_product

def test_gap_favors_low_local_competition():
    p = Product(canonical_name="childproof oven lock", niche="baby-safety")
    p.listings = [
        Listing(source="tiktok_shop", title="x", url="https://a", sold_count=5000, review_count=1200),
        Listing(source="alibaba", title="x", url="https://b", price=0.50, currency="USD", moq=50),
    ]
    score, status, parts = score_product(p)
    assert parts["algeria_gap"] == 25
    assert score > 60
