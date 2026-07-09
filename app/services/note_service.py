from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.note import Note
from app.models.user import User
from app.schemas.note import NoteCreate, NoteUpdate
from app.services.helpers import filter_for_user, get_object_or_404


def list_notes(db: Session, current_user: User) -> list[Note]:
    statement = filter_for_user(select(Note).order_by(Note.created_at.desc()), Note, current_user)
    return list(db.scalars(statement).all())


def create_note(db: Session, current_user: User, payload: NoteCreate) -> Note:
    note = Note(user_id=current_user.id, **payload.model_dump())
    db.add(note)
    db.commit()
    db.refresh(note)
    return note


def get_note(db: Session, current_user: User, note_id: UUID) -> Note:
    return get_object_or_404(db, Note, note_id, current_user)


def update_note(db: Session, current_user: User, note_id: UUID, payload: NoteUpdate) -> Note:
    note = get_note(db, current_user, note_id)
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(note, field, value)
    db.commit()
    db.refresh(note)
    return note


def delete_note(db: Session, current_user: User, note_id: UUID) -> None:
    note = get_note(db, current_user, note_id)
    db.delete(note)
    db.commit()
