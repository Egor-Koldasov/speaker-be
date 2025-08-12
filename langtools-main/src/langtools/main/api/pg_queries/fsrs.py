"""Database queries for FSRS spaced repetition data."""

from datetime import datetime
from typing import Tuple

from sqlalchemy import func, select
from sqlmodel import Session

from langtools.main.api.utils.id_generation import generate_pg_uuid
from langtools.main.fsrs import new_training_data, process_review, Rating

from ..models import Fsrs, RMeaningTranslationFsrs, DictionaryEntry, DictionaryEntryTranslation


def create_fsrs_record(
    session: Session,
    auth_user_id: str,
    dictionary_entry_translation_id: str,
    meaning_local_id: str,
) -> Tuple[Fsrs, RMeaningTranslationFsrs]:
    """Create new FSRS record for a specific meaning translation.

    Args:
        session: Database session
        auth_user_id: User ID
        dictionary_entry_translation_id: Translation record ID
        meaning_local_id: Specific meaning ID within the translation

    Returns:
        Tuple of created Fsrs and RMeaningTranslationFsrs records

    Raises:
        ValueError: If association already exists
    """
    # Check if FSRS record already exists for this meaning translation
    existing_stmt = (
        select(RMeaningTranslationFsrs)
        .where(RMeaningTranslationFsrs.auth_user_id == auth_user_id)  # type: ignore[arg-type]
        .where(
            RMeaningTranslationFsrs.dictionary_entry_translation_id
            == dictionary_entry_translation_id  # type: ignore[arg-type]
        )
        .where(RMeaningTranslationFsrs.meaning_local_id == meaning_local_id)  # type: ignore[arg-type]
    )
    existing = session.exec(existing_stmt).scalar_one_or_none()  # type: ignore[arg-type]
    if existing:
        raise ValueError("FSRS record already exists for this meaning translation")

    # Create new FSRS training data
    training_data = new_training_data()
    fsrs_id = generate_pg_uuid()

    # Create FSRS record
    fsrs = Fsrs.from_fsrs_training_data(training_data, fsrs_id)
    session.add(fsrs)

    # Create relationship record
    relationship = RMeaningTranslationFsrs(
        id=generate_pg_uuid(),
        auth_user_id=auth_user_id,
        fsrs_id=fsrs_id,
        dictionary_entry_translation_id=dictionary_entry_translation_id,
        meaning_local_id=meaning_local_id,
    )
    session.add(relationship)

    session.flush()
    return fsrs, relationship


def get_fsrs_by_id(session: Session, fsrs_id: str) -> Fsrs:
    """Get FSRS record by ID.

    Args:
        session: Database session
        fsrs_id: FSRS record ID

    Returns:
        FSRS record

    Raises:
        ValueError: If record not found
    """
    stmt = select(Fsrs).where(Fsrs.id == fsrs_id)  # type: ignore[arg-type]
    result = session.exec(stmt)  # type: ignore[arg-type]
    fsrs = result.scalar_one_or_none()
    if not fsrs:
        raise ValueError(f"FSRS record with id {fsrs_id} not found")
    return fsrs


def get_fsrs_relationship_by_fsrs_id(session: Session, fsrs_id: str) -> RMeaningTranslationFsrs:
    """Get FSRS relationship record by FSRS ID.

    Args:
        session: Database session
        fsrs_id: FSRS record ID

    Returns:
        FSRS relationship record

    Raises:
        ValueError: If relationship not found
    """
    stmt = select(RMeaningTranslationFsrs).where(
        RMeaningTranslationFsrs.fsrs_id == fsrs_id  # type: ignore[arg-type]
    )
    result = session.exec(stmt)  # type: ignore[arg-type]
    relationship = result.scalar_one_or_none()
    if not relationship:
        raise ValueError(f"FSRS relationship not found for fsrs_id {fsrs_id}")
    return relationship


def update_fsrs_from_review(
    session: Session, fsrs_id: str, rating: Rating, review_time: datetime
) -> Fsrs:
    """Update FSRS record after processing a review.

    Args:
        session: Database session
        fsrs_id: FSRS record ID
        rating: Review rating
        review_time: When review occurred

    Returns:
        Updated FSRS record

    Raises:
        ValueError: If record not found
    """
    fsrs = get_fsrs_by_id(session, fsrs_id)

    # Convert to training data, process review, convert back
    training_data = fsrs.to_fsrs_training_data()
    updated_training_data = process_review(training_data, rating, review_time)

    # Update all fields
    fsrs.due = updated_training_data.due
    fsrs.stability = updated_training_data.stability
    fsrs.difficulty = updated_training_data.difficulty
    fsrs.state = updated_training_data.state.value
    fsrs.step = updated_training_data.step
    fsrs.last_review = updated_training_data.last_review
    fsrs.reps = updated_training_data.reps
    fsrs.lapses = updated_training_data.lapses

    session.add(fsrs)
    session.flush()
    return fsrs


def get_fsrs_records_for_user(
    session: Session, auth_user_id: str, page: int = 1, page_size: int = 20
) -> Tuple[
    list[Tuple[Fsrs, RMeaningTranslationFsrs, DictionaryEntry, DictionaryEntryTranslation]], int
]:
    """Get paginated FSRS records for a user, sorted by due date.

    Args:
        session: Database session
        auth_user_id: User ID
        page: Page number (1-based)
        page_size: Number of items per page

    Returns:
        Tuple of (list of FSRS records with related data, total count)
    """
    # Base query with joins
    base_stmt = (
        select(Fsrs, RMeaningTranslationFsrs, DictionaryEntry, DictionaryEntryTranslation)
        .join(RMeaningTranslationFsrs, Fsrs.id == RMeaningTranslationFsrs.fsrs_id)  # type: ignore[arg-type]
        .join(
            DictionaryEntryTranslation,
            RMeaningTranslationFsrs.dictionary_entry_translation_id
            == DictionaryEntryTranslation.id,  # type: ignore[arg-type]
        )
        .join(DictionaryEntry, DictionaryEntryTranslation.dictionary_entry_id == DictionaryEntry.id)  # type: ignore[arg-type]
        .where(RMeaningTranslationFsrs.auth_user_id == auth_user_id)  # type: ignore[arg-type]
        .order_by(Fsrs.due.asc())  # type: ignore[attr-defined] # Soonest due first
    )

    # Get total count
    count_stmt = (
        select(func.count())
        .select_from(Fsrs)
        .join(RMeaningTranslationFsrs, Fsrs.id == RMeaningTranslationFsrs.fsrs_id)  # type: ignore[arg-type]
        .where(RMeaningTranslationFsrs.auth_user_id == auth_user_id)  # type: ignore[arg-type]
    )
    total = session.exec(count_stmt).scalar()  # type: ignore[arg-type]

    # Get paginated results
    offset = (page - 1) * page_size
    stmt = base_stmt.offset(offset).limit(page_size)
    result = session.exec(stmt)  # type: ignore[arg-type]
    records = result.all()

    return records, total or 0


def verify_meaning_translation_exists(
    session: Session, dictionary_entry_translation_id: str, meaning_local_id: str
) -> bool:
    """Verify that a meaning translation exists for the given IDs.

    Args:
        session: Database session
        dictionary_entry_translation_id: Translation record ID
        meaning_local_id: Meaning local ID to check

    Returns:
        True if the meaning exists, False otherwise
    """
    # Get the translation record
    stmt = select(DictionaryEntryTranslation).where(
        DictionaryEntryTranslation.id == dictionary_entry_translation_id  # type: ignore[arg-type]
    )
    result = session.exec(stmt)  # type: ignore[arg-type]
    translation = result.scalar_one_or_none()

    if not translation:
        return False

    # Check if meaning_local_id exists in the JSON data
    try:
        meaning_translations = translation.get_ai_meaning_translations()
        return any(mt.meaning_local_id == meaning_local_id for mt in meaning_translations)
    except Exception:
        return False
