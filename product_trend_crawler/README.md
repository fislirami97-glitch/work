# Product Trend Intelligence Crawler — MVP v0.1

A compliant, pluggable product-discovery crawler focused on finding:

**Rising abroad + cheap to source in China + weak Algerian competition**

This MVP starts with a search-API discovery layer instead of brittle anti-bot scraping.
It can search targeted domains (TikTok Shop, Amazon, Alibaba, 1688, Ouedkniss, Algerian stores),
normalize product signals, store snapshots, and calculate an opportunity score.

## Features
- Seed keyword expansion for a niche
- Domain-targeted discovery
- Product/signal normalization
- Daily snapshots
- Algeria gap score
- Trend score
- Profit/creative/sourcing/shipping scores
- Composite score /100
- FastAPI endpoints
- CLI discovery command
- SQLite by default; PostgreSQL supported via `DATABASE_URL`
- Source adapter architecture for future official API integrations

## Compliance
The project intentionally does **not** include:
- CAPTCHA solving
- anti-bot bypass
- proxy rotation to evade controls
- account/session abuse

Use official APIs where available and public crawling only where permitted.

## Quick start

### 1. Create environment
```bash
python -m venv .venv
```

Windows:
```powershell
.venv\Scripts\Activate.ps1
```

Linux/macOS:
```bash
source .venv/bin/activate
```

### 2. Install
```bash
pip install -r requirements.txt
```

### 3. Configure
Copy:
```bash
cp .env.example .env
```

Set `SERPER_API_KEY` from https://serper.dev/ if you want live discovery.

### 4. Initialize DB
```bash
python -m app.cli init-db
```

### 5. Run a discovery scan
```bash
python -m app.cli discover --niche baby-safety --limit 40
```

### 6. Start API
```bash
uvicorn app.main:app --reload
```

Open:
- `http://127.0.0.1:8000/docs`
- `http://127.0.0.1:8000/products`

## Current source strategy

| Source | MVP method | Future adapter |
|---|---|---|
| TikTok Shop | targeted web discovery | TikTok Shop API |
| Amazon | targeted web discovery | Creators API / approved product API |
| Alibaba | targeted web discovery | supplier/API feed where available |
| 1688 | targeted web discovery | approved partner/API or import |
| Ouedkniss | search-engine discovery | permitted direct integration |
| Algerian stores | targeted web discovery | per-store adapter |

## Next milestone
Add source-specific parsers for:
1. TikTok Shop sold/review signals
2. Amazon rank/review history
3. Alibaba/1688 MOQ and supplier metrics
4. Algerian competitor deduplication
5. Telegram alerts for EARLY/BREAKOUT products
