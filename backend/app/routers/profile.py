from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.components.database import get_session
from app.dto import UserProfile, UserProfileInput
from app.services import get_profile, save_profile

router = APIRouter(prefix="/api/profile", tags=["Profile"])


@router.get("", response_model=UserProfile, responses={404: {"description": "Profile not found"}})
async def read_profile(session: AsyncSession = Depends(get_session)) -> UserProfile:
    profile = await get_profile(session)
    if profile is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found")
    return profile


@router.put("", response_model=UserProfile)
async def upsert_profile(payload: UserProfileInput, session: AsyncSession = Depends(get_session)) -> UserProfile:
    try:
        profile = await save_profile(session, payload)
    except Exception as exc:  # allow FastAPI to format unexpected errors
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    return profile
