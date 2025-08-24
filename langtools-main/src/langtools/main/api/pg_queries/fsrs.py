"""Database queries for FSRS spaced repetition data."""

from datetime import datetime
from typing import Sequence, Tuple

from sqlmodel import Session, col, func, select

from langtools.main.api.utils.id_generation import generate_pg_uuid
from langtools.main.fsrs import Rating, new_training_data, process_review

from ..models import DictionaryEntry, Fsrs, RFsrsMeaning


def create_fsrs_record(
    session: Session,
    auth_user_id: str,
    dictionary_entry_id: str,
    meaning_local_id: str,
) -> Tuple[Fsrs, RFsrsMeaning]:
    """Create new FSRS record for a specific meaning translation.

    Args:
        session: Database session
        auth_user_id: User ID
        dictionary_entry_id: Translation record ID
        meaning_local_id: Specific meaning ID within the translation

    Returns:
        Tuple of created Fsrs and RMeaningTranslationFsrs records

    Raises:
        ValueError: If association already exists
    """
    # Check if FSRS record already exists for this meaning translation
    existing_stmt = (
        select(RFsrsMeaning)
        .where(RFsrsMeaning.auth_user_id == auth_user_id)
        .where(RFsrsMeaning.dictionary_entry_id == dictionary_entry_id)
        .where(RFsrsMeaning.meaning_local_id == meaning_local_id)
    )
    existing = session.exec(existing_stmt).one_or_none()
    if existing:
        raise ValueError("FSRS record already exists for this meaning")

    # Create new FSRS training data
    training_data = new_training_data()
    fsrs_id = generate_pg_uuid()

    # Create FSRS record
    fsrs = Fsrs.from_fsrs_training_data(training_data, fsrs_id)
    session.add(fsrs)

    # Create relationship record
    relationship = RFsrsMeaning(
        id=generate_pg_uuid(),
        auth_user_id=auth_user_id,
        fsrs_id=fsrs_id,
        dictionary_entry_id=dictionary_entry_id,
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
    stmt = select(Fsrs).where(Fsrs.id == fsrs_id)
    result = session.exec(stmt)
    fsrs = result.one_or_none()
    if not fsrs:
        raise ValueError(f"FSRS record with id {fsrs_id} not found")
    return fsrs


def get_fsrs_relationship_by_fsrs_id(session: Session, fsrs_id: str) -> RFsrsMeaning:
    """Get FSRS relationship record by FSRS ID.

    Args:
        session: Database session
        fsrs_id: FSRS record ID

    Returns:
        FSRS relationship record

    Raises:
        ValueError: If relationship not found
    """
    stmt = select(RFsrsMeaning).where(RFsrsMeaning.fsrs_id == fsrs_id)
    result = session.exec(stmt)
    relationship = result.one_or_none()
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
) -> Tuple[Sequence[Tuple[Fsrs, RFsrsMeaning, DictionaryEntry]], int]:
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
        select(Fsrs, RFsrsMeaning, DictionaryEntry)
        .join(RFsrsMeaning, col(RFsrsMeaning.fsrs_id) == Fsrs.id)
        .join(DictionaryEntry, col(RFsrsMeaning.dictionary_entry_id) == DictionaryEntry.id)
        .where(col(RFsrsMeaning.auth_user_id) == auth_user_id)
        .order_by(col(Fsrs.due).asc())
    )

    # Get total count
    count_stmt = (
        select(func.count())
        .select_from(Fsrs)
        .join(RFsrsMeaning, col(RFsrsMeaning.fsrs_id) == Fsrs.id)
        .where(col(RFsrsMeaning.auth_user_id) == auth_user_id)
    )
    total = session.exec(count_stmt).one()

    # Get paginated results
    offset = (page - 1) * page_size
    stmt = base_stmt.offset(offset).limit(page_size)
    result = session.exec(stmt)
    records = result.all()

    return records, total or 0


def verify_meaning_exists(
    session: Session, dictionary_entry_id: str, meaning_local_id: str
) -> bool:
    """Verify that a meaning exists for the given IDs.

    Args:
        session: Database session
        dictionary_entry_translation_id: Translation record ID
        meaning_local_id: Meaning local ID to check

    Returns:
        True if the meaning exists, False otherwise
    """
    # Get the translation record
    stmt = select(DictionaryEntry).where(col(DictionaryEntry.id) == dictionary_entry_id)
    result = session.exec(stmt)
    dictionary_entry = result.one_or_none()

    if not dictionary_entry:
        return False

    # Check if meaning_local_id exists in the JSON data
    try:
        meanings = dictionary_entry.get_ai_dictionary_entry().meanings
        return any(meaning.local_id == meaning_local_id for meaning in meanings)
    except Exception:
        return False
