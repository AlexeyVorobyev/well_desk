from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.components.database import get_session
from app.dto import Wellbeing, WellbeingInput
from app.services import get_wellbeing, save_wellbeing

router = APIRouter(prefix="/api/wellbeing", tags=["Wellbeing"])


@router.get("", response_model=Wellbeing)
async def read_wellbeing(session: AsyncSession = Depends(get_session)) -> Wellbeing:
    wellbeing = await get_wellbeing(session)
    if wellbeing is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Wellbeing not set")
    return wellbeing


@router.put("", response_model=Wellbeing)
async def upsert_wellbeing(payload: WellbeingInput, session: AsyncSession = Depends(get_session)) -> Wellbeing:
    try:
        return await save_wellbeing(session, payload)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
