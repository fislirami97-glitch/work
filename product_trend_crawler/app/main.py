from fastapi import FastAPI
from app.api.routes import router
from app.db import init_db

app = FastAPI(
    title="Product Trend Intelligence Crawler",
    version="0.1.0",
    description="Find rising international products with weak Algerian competition."
)

@app.on_event("startup")
def startup():
    init_db()

app.include_router(router)
