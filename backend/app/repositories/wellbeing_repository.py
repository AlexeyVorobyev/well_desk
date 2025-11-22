from datetime import datetime, timezone
from typing import Optional

from sqlalchemy.orm import Session

from app.models import Wellbeing
from app.settings import get_settings

settings = get_settings()
DEFAULT_USER_ID = settings.default_user_id


def get_wellbeing(session: Session, user_id: str = DEFAULT_USER_ID) -> Optional[Wellbeing]:
    return session.query(Wellbeing).filter_by(user_id=user_id).one_or_none()


def upsert_wellbeing(session: Session, data: dict, user_id: str = DEFAULT_USER_ID) -> Wellbeing:
    wellbeing = get_wellbeing(session, user_id)
    now = datetime.now(timezone.utc)

    if wellbeing is None:
        wellbeing = Wellbeing(user_id=user_id, updated_at=now, **data)
        session.add(wellbeing)
    else:
        for key, value in data.items():
            setattr(wellbeing, key, value)
        wellbeing.updated_at = now

    session.flush()
    return wellbeing
