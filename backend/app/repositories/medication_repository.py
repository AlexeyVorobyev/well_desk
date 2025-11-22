from datetime import datetime, timedelta, timezone
from typing import Iterable, Optional
from uuid import uuid4

from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import MedicationLog, MedicationReminder


async def create_reminder(
    session: AsyncSession,
    *,
    user_id: str,
    title: str,
    time: str,
    frequency: str,
) -> MedicationReminder:
    reminder = MedicationReminder(
        id=str(uuid4()),
        user_id=user_id,
        title=title,
        time=time,
        frequency=frequency,
    )
    session.add(reminder)
    await session.flush()
    return reminder


async def list_reminders(session: AsyncSession, *, user_id: str) -> Iterable[MedicationReminder]:
    result = await session.execute(
        select(MedicationReminder).where(MedicationReminder.user_id == user_id)
    )
    return result.scalars().all()


async def get_reminder(
    session: AsyncSession, reminder_id: str, *, user_id: str
) -> Optional[MedicationReminder]:
    result = await session.execute(
        select(MedicationReminder).where(
            MedicationReminder.id == reminder_id, MedicationReminder.user_id == user_id
        )
    )
    return result.scalar_one_or_none()


async def delete_reminder(session: AsyncSession, reminder: MedicationReminder) -> None:
    await session.delete(reminder)
    await session.flush()


async def create_log(
    session: AsyncSession, reminder: MedicationReminder, *, taken: bool
) -> MedicationLog:
    log = MedicationLog(id=str(uuid4()), reminder_id=reminder.id, taken=taken)
    session.add(log)
    await session.flush()
    return log


async def list_logs_for_user(
    session: AsyncSession, *, user_id: str, days: int
) -> Iterable[MedicationLog]:
    cutoff = datetime.now(timezone.utc) - timedelta(days=days)
    result = await session.execute(
        select(MedicationLog)
        .options(selectinload(MedicationLog.reminder))
        .join(MedicationReminder)
        .where(MedicationReminder.user_id == user_id, MedicationLog.timestamp >= cutoff)
        .order_by(MedicationLog.timestamp.desc())
    )
    return result.scalars().all()
