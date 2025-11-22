from sqlalchemy.ext.asyncio import AsyncSession

from app.dto import WellbeingInput
from app.repositories import wellbeing_repository


async def get_wellbeing(session: AsyncSession):
    return await wellbeing_repository.get_wellbeing(session)


async def save_wellbeing(session: AsyncSession, payload: WellbeingInput):
    data = payload.model_dump()
    wellbeing = await wellbeing_repository.upsert_wellbeing(session, data)
    await session.commit()
    await session.refresh(wellbeing)
    return wellbeing
