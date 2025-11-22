from sqlalchemy.orm import Session

from app.dto import UserProfileInput
from app.repositories import profile_repository


def get_profile(session: Session):
    return profile_repository.get_profile(session)


def save_profile(session: Session, payload: UserProfileInput):
    data = payload.model_dump(exclude_unset=True)
    return profile_repository.upsert_profile(session, data)
