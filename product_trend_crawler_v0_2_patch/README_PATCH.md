# v0.2 quality patch

This patch fixes v0.1 treating search pages, directories and generic category pages as products.

## Apply
From your project root:

```bash
cp -r /path/to/product_trend_crawler_v0_2_patch/* .
```

Then edit `.env` and use a fresh DB:

```env
DATABASE_URL=sqlite:///./crawler_v02.db
```

Run:

```bash
source .venv/bin/activate
python -m app.cli init-db
python -m app.cli discover --niche baby-safety --limit 80
```
