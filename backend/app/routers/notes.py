from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.components.database import get_session
from app.dto.note import NoteCreate, NoteRead
from app.services import note_service

router = APIRouter(prefix="/notes", tags=["notes"])


@router.post("", response_model=NoteRead, status_code=status.HTTP_201_CREATED)
def create_note_endpoint(
    payload: NoteCreate, session: Session = Depends(get_session)
) -> NoteRead:
    note = note_service.create_note(session, payload)
    return NoteRead.model_validate(note)


@router.get("", response_model=list[NoteRead])
def list_notes_endpoint(session: Session = Depends(get_session)) -> list[NoteRead]:
    notes = note_service.list_notes(session)
    return [NoteRead.model_validate(note) for note in notes]


@router.get("/{note_id}", response_model=NoteRead)
def get_note_endpoint(note_id: int, session: Session = Depends(get_session)) -> NoteRead:
    note = note_service.get_note(session, note_id)
    if note is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    return NoteRead.model_validate(note)
