from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.components.database import get_session
from app.dto import Wellbeing, WellbeingInput
from app.services import get_wellbeing, save_wellbeing

router = APIRouter(prefix="/api/wellbeing", tags=["Wellbeing"])


@router.get("", response_model=Wellbeing)
def read_wellbeing(session: Session = Depends(get_session)) -> Wellbeing:
    wellbeing = get_wellbeing(session)
    if wellbeing is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Wellbeing not set")
    return wellbeing


@router.put("", response_model=Wellbeing)
def upsert_wellbeing(payload: WellbeingInput, session: Session = Depends(get_session)) -> Wellbeing:
    try:
        return save_wellbeing(session, payload)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
