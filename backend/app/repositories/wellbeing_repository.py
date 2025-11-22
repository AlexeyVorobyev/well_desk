from datetime import datetime, timezone
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Wellbeing
from app.settings import get_settings

settings = get_settings()
DEFAULT_USER_ID = settings.default_user_id


async def get_wellbeing(session: AsyncSession, user_id: str = DEFAULT_USER_ID) -> Optional[Wellbeing]:
    return await session.get(Wellbeing, user_id)


async def upsert_wellbeing(session: AsyncSession, data: dict, user_id: str = DEFAULT_USER_ID) -> Wellbeing:
    wellbeing = await get_wellbeing(session, user_id)
    now = datetime.now(timezone.utc)

    if wellbeing is None:
        wellbeing = Wellbeing(user_id=user_id, updated_at=now, **data)
        session.add(wellbeing)
    else:
        for key, value in data.items():
            setattr(wellbeing, key, value)
        wellbeing.updated_at = now

    await session.flush()
    return wellbeing
