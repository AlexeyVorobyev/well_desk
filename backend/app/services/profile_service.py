from sqlalchemy.ext.asyncio import AsyncSession

from app.dto import UserProfileInput
from app.repositories import profile_repository


async def get_profile(session: AsyncSession):
    return await profile_repository.get_profile(session)


async def save_profile(session: AsyncSession, payload: UserProfileInput):
    data = payload.model_dump(exclude_unset=True)
    profile = await profile_repository.upsert_profile(session, data)
    await session.commit()
    await session.refresh(profile)
    return profile
