from fastapi import FastAPI

from app.db import engine
from app.models import Base
from app.routers import emails

# Create tables on startup
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Mail2Audio")

# API routes only
app.include_router(emails.router, prefix="/api", tags=["emails"])
# app.include_router(auth.router, prefix="/auth", tags=["auth"])  # Add when ready


@app.get("/health")
def health_check():
    return {"status": "healthy"}
