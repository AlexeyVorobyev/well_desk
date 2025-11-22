from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.components.database import get_session
from app.dto import MedicationLog, MedicationLogInput, MedicationReminder, MedicationReminderInput
from app.services import (
    create_medication_reminder,
    list_medication_logs,
    list_medication_reminders,
    log_medication_intake,
    remove_medication_reminder,
)

router = APIRouter(prefix="/api/medications", tags=["Medications"])


@router.post("", response_model=MedicationReminder, status_code=status.HTTP_201_CREATED)
async def create_reminder(
    payload: MedicationReminderInput, session: AsyncSession = Depends(get_session)
) -> MedicationReminder:
    return await create_medication_reminder(session, payload)


@router.get("", response_model=list[MedicationReminder])
async def get_reminders(session: AsyncSession = Depends(get_session)) -> list[MedicationReminder]:
    reminders = await list_medication_reminders(session)
    return list(reminders)


@router.delete("/{reminder_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_reminder(reminder_id: str, session: AsyncSession = Depends(get_session)) -> None:
    try:
        await remove_medication_reminder(session, reminder_id)
    except LookupError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.post("/{reminder_id}/log", response_model=MedicationLog)
async def log_reminder(
    reminder_id: str, payload: MedicationLogInput, session: AsyncSession = Depends(get_session)
) -> MedicationLog:
    try:
        return await log_medication_intake(session, reminder_id, payload)
    except LookupError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.get("/logs", response_model=list[MedicationLog])
async def get_logs(
    days: int = Query(7, ge=1, le=90), session: AsyncSession = Depends(get_session)
) -> list[MedicationLog]:
    return list(await list_medication_logs(session, days=days))
