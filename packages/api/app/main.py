from fastapi import FastAPI

from app.routers import emails

# Schema is owned by Alembic -- run `alembic upgrade head` to create or update
# it. Creating tables here on import would silently diverge from the migration
# history and, worse, would do so as a side effect of merely importing the app
# (which is what test collection does).

app = FastAPI(title="Mail2Audio")

# API routes only
app.include_router(emails.router, prefix="/api", tags=["emails"])
# app.include_router(auth.router, prefix="/auth", tags=["auth"])  # Add when ready


@app.get("/health")
def health_check():
    return {"status": "healthy"}
