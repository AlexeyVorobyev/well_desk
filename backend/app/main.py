from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse

from app.components.database import Base, engine
from app.routers import messages, profile, wellbeing
from app.settings import get_settings

settings = get_settings()
app = FastAPI(title=settings.app_name, debug=settings.debug)


@app.on_event("startup")
async def on_startup() -> None:
    """Initialize database metadata on application startup."""

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.exception_handler(HTTPException)
async def format_http_exceptions(request: Request, exc: HTTPException) -> JSONResponse:
    """Return errors using the shared ErrorMessage schema."""

    detail = exc.detail
    if isinstance(detail, dict):
        message = detail.get("message", str(detail))
    else:
        message = str(detail)

    return JSONResponse(status_code=exc.status_code, content={"message": message})


app.include_router(profile.router)
app.include_router(messages.router)
app.include_router(wellbeing.router)
