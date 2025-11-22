from datetime import datetime, timezone
from typing import Optional

from sqlalchemy.orm import Session

from app.models import UserProfile
from app.settings import get_settings

settings = get_settings()
DEFAULT_USER_ID = settings.default_user_id


def get_profile(session: Session, user_id: str = DEFAULT_USER_ID) -> Optional[UserProfile]:
    return session.query(UserProfile).filter_by(id=user_id).one_or_none()


def upsert_profile(session: Session, data: dict, user_id: str = DEFAULT_USER_ID) -> UserProfile:
    profile = get_profile(session, user_id)
    now = datetime.now(timezone.utc)

    if profile is None:
        profile = UserProfile(id=user_id, created_at=now, updated_at=now, **data)
        session.add(profile)
    else:
        for key, value in data.items():
            setattr(profile, key, value)
        profile.updated_at = now

    session.flush()
    return profile
