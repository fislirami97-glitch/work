from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.db import SessionLocal
from app.models import Product
from app.services.pipeline import discover as discover_pipeline

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/health")
def health():
    return {"status": "ok"}

@router.get("/products")
def products(
    min_score: float = Query(0, ge=0, le=100),
    status: str | None = None,
    db: Session = Depends(get_db)
):
    stmt = select(Product).where(Product.score >= min_score).order_by(Product.score.desc())
    if status:
        stmt = stmt.where(Product.status == status)
    rows = db.scalars(stmt).all()
    return [
        {
            "id": p.id,
            "name": p.canonical_name,
            "niche": p.niche,
            "status": p.status,
            "score": p.score,
            "sources": sorted({x.source for x in p.listings}),
            "listing_count": len(p.listings),
        } for p in rows
    ]

@router.post("/discover")
async def run_discovery(
    niche: str = "baby-safety",
    limit: int = Query(40, ge=1, le=200),
    db: Session = Depends(get_db)
):
    products = await discover_pipeline(db, niche=niche, limit=limit)
    return {
        "ok": True,
        "products_total": len(products),
        "top": [
            {"id": p.id, "name": p.canonical_name, "score": p.score, "status": p.status}
            for p in sorted(products, key=lambda x: x.score, reverse=True)[:10]
        ]
    }
