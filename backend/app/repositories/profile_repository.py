from datetime import datetime, timezone
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.models import UserProfile
from app.settings import get_settings

settings = get_settings()
DEFAULT_USER_ID = settings.default_user_id


async def get_profile(session: AsyncSession, user_id: str = DEFAULT_USER_ID) -> Optional[UserProfile]:
    return await session.get(UserProfile, user_id)


async def upsert_profile(session: AsyncSession, data: dict, user_id: str = DEFAULT_USER_ID) -> UserProfile:
    profile = await get_profile(session, user_id)
    now = datetime.now(timezone.utc)

    if profile is None:
        profile = UserProfile(id=user_id, created_at=now, updated_at=now, **data)
        session.add(profile)
    else:
        for key, value in data.items():
            setattr(profile, key, value)
        profile.updated_at = now

    await session.flush()
    return profile
