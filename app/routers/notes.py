from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.note import NoteCreate, NoteRead, NoteUpdate
from app.services.note_service import create_note, delete_note, get_note, list_notes, update_note

router = APIRouter(prefix="/notes", tags=["Notes"])


@router.get("/", response_model=list[NoteRead])
def read_notes(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return list_notes(db, current_user)


@router.post("/", response_model=NoteRead, status_code=status.HTTP_201_CREATED)
def create_new_note(
    payload: NoteCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return create_note(db, current_user, payload)


@router.get("/{note_id}", response_model=NoteRead)
def read_note(note_id: UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_note(db, current_user, note_id)


@router.patch("/{note_id}", response_model=NoteRead)
def edit_note(
    note_id: UUID,
    payload: NoteUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return update_note(db, current_user, note_id, payload)


@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_note(note_id: UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    delete_note(db, current_user, note_id)
