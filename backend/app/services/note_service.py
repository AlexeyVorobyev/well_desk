from sqlalchemy.orm import Session

from app.components.llm import summarizer
from app.dto.note import NoteCreate
from app.models.note import Note
from app.repositories.note_repository import NoteRepository


def create_note(session: Session, payload: NoteCreate) -> Note:
    repository = NoteRepository(session)
    summary = summarizer.summarize(payload.content)

    note = Note(title=payload.title, content=payload.content, summary=summary)
    return repository.add(note)


def list_notes(session: Session) -> list[Note]:
    repository = NoteRepository(session)
    return list(repository.list())


def get_note(session: Session, note_id: int) -> Note | None:
    repository = NoteRepository(session)
    return repository.get(note_id)
