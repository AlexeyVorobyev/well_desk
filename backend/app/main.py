from fastapi import FastAPI

from app.components.database import Base, engine
from app.routers import notes
from app.settings import get_settings

settings = get_settings()
app = FastAPI(title=settings.app_name, debug=settings.debug)


@app.on_event("startup")
def on_startup() -> None:
    Base.metadata.create_all(bind=engine)


app.include_router(notes.router)
