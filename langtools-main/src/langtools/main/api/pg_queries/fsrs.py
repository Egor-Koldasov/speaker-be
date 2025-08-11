"""Database queries for FSRS training data and relations."""

from datetime import datetime
from typing import Optional

from sqlalchemy import and_, select
from sqlmodel import Session

from langtools.main.fsrs.models import FSRSCardState, FSRSTrainingData

from ..models.fsrs import FSRS, RMeaningTranslationFSRS
from ..utils.id_generation import generate_pg_uuid


def fsrs_to_training_data(fsrs: FSRS) -> FSRSTrainingData:
    """Convert FSRS row to domain training data."""
    return FSRSTrainingData(
        due=fsrs.due,
        stability=fsrs.stability,
        difficulty=fsrs.difficulty,
        state=FSRSCardState(fsrs.state),
        step=fsrs.step,
        last_review=fsrs.last_review,
        reps=fsrs.reps,
        lapses=fsrs.lapses,
    )


def training_data_to_fsrs_row(fsrs_id: str, data: FSRSTrainingData) -> FSRS:
    """Create FSRS row from training data."""
    return FSRS(
        id=fsrs_id,
        due=data.due,
        stability=data.stability,
        difficulty=data.difficulty,
        state=int(data.state),
        step=data.step,
        last_review=data.last_review,
        reps=data.reps,
        lapses=data.lapses,
    )


def create_fsrs(
    session: Session,
    auth_user_id: str,
    dictionary_entry_translation_id: str,
    meaning_local_id: str,
    initial_data: FSRSTrainingData,
) -> tuple[FSRS, RMeaningTranslationFSRS]:
    """Create new FSRS record and relation row."""
    fsrs_id = generate_pg_uuid()
    fsrs_row = training_data_to_fsrs_row(fsrs_id, initial_data)
    session.add(fsrs_row)

    rel = RMeaningTranslationFSRS(
        id=generate_pg_uuid(),
        auth_user_id=auth_user_id,
        fsrs_id=fsrs_id,
        dictionary_entry_translation_id=dictionary_entry_translation_id,
        meaning_local_id=meaning_local_id,
    )
    session.add(rel)

    session.flush()
    return fsrs_row, rel


def get_fsrs_by_relation(
    session: Session,
    auth_user_id: str,
    dictionary_entry_translation_id: str,
    meaning_local_id: str,
) -> Optional[FSRS]:
    """Find FSRS by unique relation for user and translation meaning."""
    stmt = (
        select(FSRS)
        .join(RMeaningTranslationFSRS, RMeaningTranslationFSRS.fsrs_id == FSRS.id)  # type: ignore[arg-type]
        .where(
            and_(
                RMeaningTranslationFSRS.auth_user_id == auth_user_id,  # type: ignore[arg-type]
                RMeaningTranslationFSRS.dictionary_entry_translation_id
                == dictionary_entry_translation_id,  # type: ignore[arg-type]
                RMeaningTranslationFSRS.meaning_local_id == meaning_local_id,  # type: ignore[arg-type]
            )
        )
    )
    result = session.exec(stmt)  # type: ignore[arg-type]
    return result.scalar_one_or_none()


def get_fsrs_by_id(session: Session, auth_user_id: str, fsrs_id: str) -> Optional[FSRS]:
    """Find FSRS by ID for a user (via relation)."""
    stmt = (
        select(FSRS)
        .join(RMeaningTranslationFSRS, RMeaningTranslationFSRS.fsrs_id == FSRS.id)  # type: ignore[arg-type]
        .where(
            and_(
                RMeaningTranslationFSRS.auth_user_id == auth_user_id,  # type: ignore[arg-type]
                RMeaningTranslationFSRS.fsrs_id == fsrs_id,  # type: ignore[arg-type]
            )
        )
    )
    result = session.exec(stmt)  # type: ignore[arg-type]
    return result.scalar_one_or_none()


def update_fsrs_from_training_data(
    session: Session, fsrs_row: FSRS, data: FSRSTrainingData
) -> FSRS:
    """Update an FSRS row with new training data fields."""
    fsrs_row.due = data.due
    fsrs_row.stability = data.stability
    fsrs_row.difficulty = data.difficulty
    fsrs_row.state = int(data.state)
    fsrs_row.step = data.step
    fsrs_row.last_review = data.last_review
    fsrs_row.reps = data.reps
    fsrs_row.lapses = data.lapses
    fsrs_row.updated_at = datetime.now()
    session.add(fsrs_row)
    session.flush()
    return fsrs_row


def list_user_fsrs_sorted_by_due(
    session: Session,
    auth_user_id: str,
    limit: int,
    offset: int,
) -> list[FSRS]:
    """List user's FSRS rows sorted by due ascending with pagination."""
    stmt = (
        select(FSRS)
        .join(RMeaningTranslationFSRS, RMeaningTranslationFSRS.fsrs_id == FSRS.id)  # type: ignore[arg-type]
        .where(RMeaningTranslationFSRS.auth_user_id == auth_user_id)  # type: ignore[arg-type]
        .order_by(FSRS.due.asc())  # type: ignore[attr-defined]
        .limit(limit)
        .offset(offset)
    )
    result = session.exec(stmt)  # type: ignore[arg-type]
    return list(result.scalars().all())


def get_relation_by_fsrs_id(
    session: Session, auth_user_id: str, fsrs_id: str
) -> Optional[RMeaningTranslationFSRS]:
    """Get relation row for a user's FSRS id."""
    stmt = (
        select(RMeaningTranslationFSRS)
        .where(RMeaningTranslationFSRS.auth_user_id == auth_user_id)  # type: ignore[arg-type]
        .where(RMeaningTranslationFSRS.fsrs_id == fsrs_id)  # type: ignore[arg-type]
        .limit(1)
    )
    result = session.exec(stmt)  # type: ignore[arg-type]
    return result.scalar_one_or_none()
