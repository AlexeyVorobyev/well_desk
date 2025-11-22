from typing import Iterable

from sqlalchemy.ext.asyncio import AsyncSession

from app.dto import MedicationLog, MedicationLogInput, MedicationReminder, MedicationReminderInput
from app.repositories import (
    DEFAULT_USER_ID,
    create_log,
    create_reminder,
    delete_reminder,
    get_reminder,
    list_logs_for_user,
    list_reminders,
)


async def create_medication_reminder(
    session: AsyncSession, payload: MedicationReminderInput, *, user_id: str = DEFAULT_USER_ID
) -> MedicationReminder:
    reminder = await create_reminder(
        session,
        user_id=user_id,
        title=payload.title.strip(),
        time=payload.time,
        frequency=payload.frequency,
    )
    await session.commit()
    await session.refresh(reminder)
    return reminder


async def list_medication_reminders(
    session: AsyncSession, *, user_id: str = DEFAULT_USER_ID
) -> Iterable[MedicationReminder]:
    reminders = await list_reminders(session, user_id=user_id)
    return reminders


async def remove_medication_reminder(
    session: AsyncSession, reminder_id: str, *, user_id: str = DEFAULT_USER_ID
) -> None:
    reminder = await get_reminder(session, reminder_id, user_id=user_id)
    if reminder is None:
        raise LookupError("Reminder not found")

    await delete_reminder(session, reminder)
    await session.commit()


async def log_medication_intake(
    session: AsyncSession, reminder_id: str, payload: MedicationLogInput, *, user_id: str = DEFAULT_USER_ID
) -> MedicationLog:
    reminder = await get_reminder(session, reminder_id, user_id=user_id)
    if reminder is None:
        raise LookupError("Reminder not found")

    log = await create_log(session, reminder, taken=payload.taken)
    await session.commit()
    await session.refresh(log)

    # Attach reminder info for client convenience
    log.reminder = reminder
    log.reminder_title = reminder.title  # type: ignore[attr-defined]
    log.reminder_time = reminder.time  # type: ignore[attr-defined]
    return log


async def list_medication_logs(
    session: AsyncSession, *, days: int = 7, user_id: str = DEFAULT_USER_ID
) -> Iterable[MedicationLog]:
    if days < 1:
        raise ValueError("Days must be at least 1")

    logs = await list_logs_for_user(session, user_id=user_id, days=days)
    # Enrich logs with reminder references for serialization
    for log in logs:
        if log.reminder is not None:
            log.reminder_title = log.reminder.title  # type: ignore[attr-defined]
            log.reminder_time = log.reminder.time  # type: ignore[attr-defined]
    return logs
