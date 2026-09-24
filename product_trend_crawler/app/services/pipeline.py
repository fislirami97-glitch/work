import asyncio
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.collectors.serper import SerperCollector
from app.models import Product, Listing, Snapshot
from app.services.config import load_config
from app.services.normalize import canonicalize_title, infer_source
from app.services.extract import enrich_from_text
from app.services.scoring import score_product

async def discover(session: Session, niche: str = "baby-safety", limit: int = 30):
    cfg = load_config()
    niche_cfg = cfg["niches"][niche]
    collector = SerperCollector()

    tasks = []
    per_query = max(3, min(10, limit // max(1, len(niche_cfg["seeds"]) // 2)))
    for seed in niche_cfg["seeds"]:
        for src_name, src in cfg["sources"].items():
            for domain in src["domains"]:
                tasks.append((src_name, seed, domain, collector.search(seed, domain, per_query)))

    discovered = []
    for src_name, seed, domain, coro in tasks:
        try:
            rows = await coro
            for row in rows:
                row.source = src_name
                discovered.append(enrich_from_text(row))
        except Exception as e:
            print(f"[warn] {src_name} {domain} {seed}: {e}")

    # Dedup by URL before DB
    unique = {}
    for item in discovered:
        if item.url:
            unique[item.url] = item

    for item in list(unique.values())[:limit]:
        exists = session.scalar(select(Listing).where(Listing.url == item.url))
        if exists:
            session.add(Snapshot(
                listing_id=exists.id,
                price=item.price,
                sold_count=item.sold_count,
                review_count=item.review_count,
                rating=item.rating,
            ))
            continue

        canonical = canonicalize_title(item.title)
        product = session.scalar(
            select(Product).where(
                Product.canonical_name == canonical,
                Product.niche == niche
            )
        )
        if not product:
            product = Product(canonical_name=canonical, niche=niche)
            session.add(product)
            session.flush()

        listing = Listing(
            product_id=product.id,
            source=item.source,
            title=item.title,
            url=item.url,
            snippet=item.snippet,
            price=item.price,
            currency=item.currency,
            sold_count=item.sold_count,
            review_count=item.review_count,
            rating=item.rating,
            moq=item.moq,
        )
        session.add(listing)
        session.flush()
        session.add(Snapshot(
            listing_id=listing.id,
            price=listing.price,
            sold_count=listing.sold_count,
            review_count=listing.review_count,
            rating=listing.rating,
        ))

    session.commit()

    products = session.scalars(select(Product)).all()
    for product in products:
        total, status, _ = score_product(product)
        product.score = total
        product.status = status
    session.commit()

    return products
