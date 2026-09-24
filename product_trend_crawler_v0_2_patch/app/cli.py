import asyncio
import typer
from rich.console import Console
from rich.table import Table
from app.db import init_db, SessionLocal
from app.services.pipeline import discover as discover_pipeline

app = typer.Typer(no_args_is_help=True)
console = Console()

@app.command("init-db")
def init_db_cmd():
    init_db(); console.print("[green]Database initialized.[/green]")

@app.command()
def discover(niche: str = typer.Option("baby-safety"), limit: int = typer.Option(80, min=1, max=300)):
    init_db()
    with SessionLocal() as db:
        products = asyncio.run(discover_pipeline(db, niche=niche, limit=limit))
        top = sorted(products, key=lambda x: (x.score, x.confidence), reverse=True)[:25]
        table = Table(title=f"Top opportunities — {niche} (v0.2)")
        for col in ["Score","Conf.","Status","Product","Sources"]: table.add_column(col)
        for p in top:
            table.add_row(f"{p.score:.1f}", f"{p.confidence:.0f}", p.status,
                          p.canonical_name[:72], ", ".join(sorted({x.source for x in p.listings})))
        console.print(table)

if __name__ == "__main__": app()
