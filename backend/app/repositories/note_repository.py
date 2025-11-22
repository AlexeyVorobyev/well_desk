from typing import Iterable, Optional

from sqlalchemy.orm import Session

from app.models.note import Note


class NoteRepository:
    """Data access layer for notes."""

    def __init__(self, session: Session):
        self.session = session

    def add(self, note: Note) -> Note:
        self.session.add(note)
        self.session.flush()
        self.session.refresh(note)
        return note

    def list(self) -> Iterable[Note]:
        return self.session.query(Note).order_by(Note.created_at.desc()).all()

    def get(self, note_id: int) -> Optional[Note]:
        return self.session.query(Note).filter(Note.id == note_id).first()
