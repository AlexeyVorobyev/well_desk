from fastapi import FastAPI

from app.components.database import Base, engine
from app.settings import get_settings

settings = get_settings()
app = FastAPI(title=settings.app_name, debug=settings.debug)


@app.on_event("startup")
def on_startup() -> None:
    """Initialize database metadata on application startup."""

    Base.metadata.create_all(bind=engine)


# Routers can be included here using app.include_router(...)
