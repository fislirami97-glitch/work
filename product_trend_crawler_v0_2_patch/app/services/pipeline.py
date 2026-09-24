from sqlalchemy import select
from app.collectors.serper import SerperCollector
from app.models import Product, Listing, Snapshot
from app.services.config import load_config
from app.services.querying import build_query
from app.services.quality import looks_like_product_page
from app.services.normalize import canonicalize_title, similarity
from app.services.extract import enrich_from_text
from app.services.scoring import score_product

def find_cluster(session, niche, canonical):
    existing = session.scalars(select(Product).where(Product.niche == niche)).all()
    best, best_sim = None, 0.0
    for p in existing:
        sim = similarity(canonical, p.canonical_name)
        if sim > best_sim:
            best, best_sim = p, sim
    return best if best_sim >= 0.50 else None

async def discover(session, niche="baby-safety", limit=80):
    cfg = load_config(); collector = SerperCollector(); found = []
    for seed in cfg["niches"][niche]["seeds"]:
        for src_name, src in cfg["sources"].items():
            q = build_query(src_name, seed)
            for domain in src["domains"]:
                try:
                    rows = await collector.search(q, domain, 8)
                    for row in rows:
                        row.source = src_name
                        row = enrich_from_text(row)
                        if looks_like_product_page(src_name, row.url, row.title):
                            found.append(row)
                except Exception as e:
                    print(f"[warn] {src_name} {domain} {seed}: {e}")

    unique = {x.url: x for x in found if x.url}
    for item in list(unique.values())[:limit]:
        exists = session.scalar(select(Listing).where(Listing.url == item.url))
        if exists:
            session.add(Snapshot(listing_id=exists.id, price=item.price, sold_count=item.sold_count, review_count=item.review_count, rating=item.rating))
            continue
        canonical = canonicalize_title(item.title)
        product = find_cluster(session, niche, canonical)
        if not product:
            product = Product(canonical_name=canonical, niche=niche)
            session.add(product); session.flush()
        listing = Listing(product_id=product.id, source=item.source, title=item.title, url=item.url,
                          snippet=item.snippet, price=item.price, currency=item.currency,
                          sold_count=item.sold_count, review_count=item.review_count,
                          rating=item.rating, moq=item.moq)
        session.add(listing); session.flush()
        session.add(Snapshot(listing_id=listing.id, price=listing.price, sold_count=listing.sold_count,
                             review_count=listing.review_count, rating=listing.rating))
    session.commit()

    products = session.scalars(select(Product)).all()
    for p in products:
        p.score, p.confidence, p.status = score_product(p)
    session.commit()
    return products
