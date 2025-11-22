from sqlalchemy.orm import Session

from app.dto import WellbeingInput
from app.repositories import wellbeing_repository


def get_wellbeing(session: Session):
    return wellbeing_repository.get_wellbeing(session)


def save_wellbeing(session: Session, payload: WellbeingInput):
    data = payload.model_dump()
    return wellbeing_repository.upsert_wellbeing(session, data)
