"""Database queries for FSRS data and associations."""

from datetime import datetime, timezone
from typing import Optional

from sqlmodel import Session, select

from ..models import DictionaryEntryTranslation
from ..models.fsrs import FSRS, RMeaningTranslationFSRS
from ..utils.id_generation import generate_pg_uuid


class FSRSConflictError(Exception):
    """Raised when trying to create a duplicate FSRS association for the same meaning."""


def create_fsrs(training_data: dict[str, object]) -> FSRS:
    """Create FSRS row from dict fields.

    Expects keys: due, stability, difficulty, state, step, last_review, reps, lapses.
    """

    return FSRS(
        id=generate_pg_uuid(),
        due=training_data["due"],  # type: ignore[arg-type]
        stability=training_data.get("stability")
        if training_data.get("stability") is not None
        else None,  # type: ignore[return-value]
        difficulty=training_data.get("difficulty")
        if training_data.get("difficulty") is not None
        else None,  # type: ignore[return-value]
        state=int(training_data["state"]),  # type: ignore[arg-type]
        step=int(training_data["step"]),  # type: ignore[arg-type]
        last_review=training_data.get("last_review"),  # type: ignore[assignment]
        reps=int(training_data.get("reps", 0)),  # type: ignore[arg-type]
        lapses=int(training_data.get("lapses", 0)),  # type: ignore[arg-type]
    )


def upsert_fsrs_for_meaning(
    session: Session,
    auth_user_id: str,
    dictionary_entry_translation_id: str,
    meaning_local_id: str,
    training_data: dict[str, object],
) -> FSRS:
    """Create a new FSRS record and link it to a meaning translation if not exists.

    If association exists, raise FSRSConflictError to signal duplicate.
    """

    # Check translation exists
    stmt_tr = select(DictionaryEntryTranslation).where(
        DictionaryEntryTranslation.id == dictionary_entry_translation_id
    )
    translation = session.exec(stmt_tr).first()
    if translation is None:
        raise ValueError("dictionary_entry_translation not found")

    # Check existing link
    stmt = select(RMeaningTranslationFSRS).where(
        (RMeaningTranslationFSRS.auth_user_id == auth_user_id)
        & (
            RMeaningTranslationFSRS.dictionary_entry_translation_id
            == dictionary_entry_translation_id
        )
        & (RMeaningTranslationFSRS.meaning_local_id == meaning_local_id)
    )
    existing = session.exec(stmt).first()
    if existing is not None:
        raise FSRSConflictError("FSRS already exists for this meaning translation")

    # Create FSRS
    fsrs = create_fsrs(training_data)
    session.add(fsrs)

    # Link
    link = RMeaningTranslationFSRS(
        id=generate_pg_uuid(),
        auth_user_id=auth_user_id,
        fsrs_id=fsrs.id,
        dictionary_entry_translation_id=dictionary_entry_translation_id,
        meaning_local_id=meaning_local_id,
    )
    session.add(link)
    session.flush()
    return fsrs


def list_fsrs_for_user(
    session: Session, auth_user_id: str, limit: int = 50, offset: int = 0
) -> list[tuple[FSRS, RMeaningTranslationFSRS, DictionaryEntryTranslation]]:
    """Return FSRS items for user along with association and translation rows.

    Sorted by due ascending.
    """
    stmt = (
        select(FSRS, RMeaningTranslationFSRS, DictionaryEntryTranslation)
        .where(RMeaningTranslationFSRS.auth_user_id == auth_user_id)
        .where(FSRS.id == RMeaningTranslationFSRS.fsrs_id)
        .where(
            DictionaryEntryTranslation.id == RMeaningTranslationFSRS.dictionary_entry_translation_id
        )
        .order_by(FSRS.due.asc())
        .limit(limit)
        .offset(offset)
    )
    rows = session.exec(stmt).all()
    return rows


def get_fsrs_by_id(session: Session, fsrs_id: str) -> Optional[FSRS]:
    return session.get(FSRS, fsrs_id)


def update_fsrs_from_training_data(
    fsrs: FSRS, training_data: dict[str, object], review_time: datetime | None = None
) -> FSRS:
    # Persist naive UTC
    due_dt = training_data["due"]  # type: ignore[index]
    if isinstance(due_dt, datetime) and due_dt.tzinfo is not None:
        due_dt = due_dt.astimezone(timezone.utc).replace(tzinfo=None)
    fsrs.due = due_dt  # type: ignore[assignment]
    fsrs.stability = (
        training_data.get("stability") if training_data.get("stability") is not None else None
    )  # type: ignore[assignment]
    fsrs.difficulty = (
        training_data.get("difficulty") if training_data.get("difficulty") is not None else None
    )  # type: ignore[assignment]
    fsrs.state = int(training_data["state"])  # type: ignore[assignment]
    fsrs.step = int(training_data["step"])  # type: ignore[assignment]
    lr = training_data.get("last_review")
    if isinstance(lr, datetime) and lr.tzinfo is not None:
        lr = lr.astimezone(timezone.utc).replace(tzinfo=None)
    fsrs.last_review = lr  # type: ignore[assignment]
    fsrs.reps = int(training_data.get("reps", fsrs.reps))  # type: ignore[assignment]
    fsrs.lapses = int(training_data.get("lapses", fsrs.lapses))  # type: ignore[assignment]
    return fsrs
