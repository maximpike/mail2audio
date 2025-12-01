from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from app.models.base import engine, Base
from app.routers import landing, emails, dashboard

# Create tables on startup
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Mail2Audio")

# How does this work with FE bundling and loading NB!!
BASE_DIR = Path(__file__).resolve().parent.parent

app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
app.include_router(landing.router, tags=["landing"]) # How does this work

app.include_router(emails.router, tags=["emails"])
app.include_router(dashboard.router, tags=["dashboard"])

@app.get("/health")
def health_check():
    return {"status": "healthy"}

