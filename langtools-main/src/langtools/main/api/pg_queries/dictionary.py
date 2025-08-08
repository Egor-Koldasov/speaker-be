"""Database queries for dictionary entries."""

from datetime import datetime
from typing import cast, TypedDict

from sqlmodel import Session, select, desc, func

from langtools.ai.models import AiDictionaryEntry, AiMeaningTranslation
from langtools.main.api.models import (
    DictionaryEntry,
    DictionaryEntryTranslation,
    MeaningFSRS,
    UserDictionaryEntry,
)
from langtools.main.api.utils.id_generation import generate_uuidv7
from langtools.main.fsrs.functions import new_training_data, process_review
from langtools.main.fsrs.models import Rating, FSRSTrainingData, FSRSCardState


class EntryDataDict(TypedDict, total=False):
    """Type for dictionary entry JSON data."""

    headword: str
    source_language: str
    meanings: list[dict[str, object]]


async def create_dictionary_entry(
    db: Session,
    auth_user_id: str,
    entry: AiDictionaryEntry,
    translations: list[AiMeaningTranslation],
) -> str:
    """Create a dictionary entry with all related data.

    Creates entries in:
    - dictionary_entry
    - user_dictionary_entry
    - dictionary_entry_translation
    - meaning_fsrs (one per meaning)

    Args:
        db: Database session
        auth_user_id: ID of the user creating the entry
        entry: Base dictionary entry
        translations: Translations for all meanings

    Returns:
        ID of the created dictionary entry

    Raises:
        ValueError: If validation fails
    """
    # Validate that all meanings have translations
    meaning_ids = {meaning.local_id for meaning in entry.meanings}
    translation_meaning_ids = {trans.meaning_local_id for trans in translations}

    if meaning_ids != translation_meaning_ids:
        missing = meaning_ids - translation_meaning_ids
        extra = translation_meaning_ids - meaning_ids
        raise ValueError(
            f"Translation validation failed. Missing translations for: {missing}. "
            f"Extra translations for: {extra}."
        )

    # Create dictionary entry
    entry_id = generate_uuidv7()
    dict_entry = DictionaryEntry(
        id=entry_id,
        json_data=entry.model_dump(),
    )
    db.add(dict_entry)

    # Create user-dictionary entry relationship
    user_dict_entry = UserDictionaryEntry(
        id=generate_uuidv7(),
        auth_user_id=auth_user_id,
        dictionary_entry_id=entry_id,
    )
    db.add(user_dict_entry)

    # Create dictionary entry translations
    dict_entry_translation = DictionaryEntryTranslation(
        id=generate_uuidv7(),
        dictionary_entry_id=entry_id,
        json_data=[trans.model_dump() for trans in translations],
    )
    db.add(dict_entry_translation)

    # Create FSRS training data for each meaning
    for _ in entry.meanings:
        # Initialize new FSRS training data
        fsrs_data = new_training_data()

        meaning_fsrs = MeaningFSRS(
            id=generate_uuidv7(),
            dictionary_entry_id=entry_id,
            due=fsrs_data.due,
            stability=fsrs_data.stability,
            difficulty=fsrs_data.difficulty,
            state=fsrs_data.state,
            step=fsrs_data.step,
            last_review=fsrs_data.last_review,
            reps=fsrs_data.reps,
            lapses=fsrs_data.lapses,
        )
        db.add(meaning_fsrs)

    # Commit all changes
    db.commit()

    return entry_id


def get_dictionary_entry(db: Session, auth_user_id: str, entry_id: str) -> dict[str, object] | None:
    """Get a dictionary entry with translations.

    Args:
        db: Database session
        auth_user_id: ID of the requesting user
        entry_id: ID of the dictionary entry

    Returns:
        Dictionary with entry data and translations, or None if not found
    """
    # Check if user has access to this entry
    stmt = select(UserDictionaryEntry).where(
        UserDictionaryEntry.auth_user_id == auth_user_id,
        UserDictionaryEntry.dictionary_entry_id == entry_id,
    )
    user_entry = db.exec(stmt).first()

    if not user_entry:
        return None

    # Get the dictionary entry
    stmt = select(DictionaryEntry).where(DictionaryEntry.id == entry_id)
    entry = db.exec(stmt).first()
    if not entry:
        return None

    # Get translations
    stmt = select(DictionaryEntryTranslation).where(
        DictionaryEntryTranslation.dictionary_entry_id == entry_id
    )
    translation = db.exec(stmt).first()

    return {
        "id": entry.id,
        "entry": entry.json_data,
        "translations": translation.json_data if translation else [],
        "created_at": entry.created_at,
        "updated_at": entry.updated_at,
    }


def list_user_dictionary_entries(
    db: Session, auth_user_id: str, page: int = 1, page_size: int = 20
) -> dict[str, object]:
    """List user's dictionary entries with pagination.

    Args:
        db: Database session
        auth_user_id: ID of the requesting user
        page: Page number (1-based)
        page_size: Number of items per page

    Returns:
        Dictionary with entries list and pagination info
    """
    # Base query for user's entries
    stmt = (
        select(DictionaryEntry)
        .join(UserDictionaryEntry)
        .where(UserDictionaryEntry.auth_user_id == auth_user_id)
    )

    # Get total count
    count_stmt = select(func.count()).select_from(stmt.subquery())
    total = db.exec(count_stmt).one()

    # Get paginated entries
    offset = (page - 1) * page_size
    stmt = stmt.offset(offset).limit(page_size).order_by(desc(DictionaryEntry.created_at))
    entries = db.exec(stmt).all()

    # Build response
    entry_items = []
    for entry in entries:
        entry_data = cast(EntryDataDict, entry.json_data)
        entry_items.append(
            {
                "id": entry.id,
                "headword": entry_data.get("headword", ""),
                "source_language": entry_data.get("source_language", ""),
                "meanings_count": len(entry_data.get("meanings", [])),
                "created_at": entry.created_at,
                "updated_at": entry.updated_at,
            }
        )

    return {
        "entries": entry_items,
        "total": total,
        "page": page,
        "page_size": page_size,
    }


def get_dictionary_entry_fsrs(
    db: Session, auth_user_id: str, entry_id: str
) -> list[dict[str, object]] | None:
    """Get FSRS data for all meanings of a dictionary entry.

    Args:
        db: Database session
        auth_user_id: ID of the requesting user
        entry_id: ID of the dictionary entry

    Returns:
        List of FSRS data for each meaning, or None if not authorized
    """
    # Check if user has access to this entry
    stmt = select(UserDictionaryEntry).where(
        UserDictionaryEntry.auth_user_id == auth_user_id,
        UserDictionaryEntry.dictionary_entry_id == entry_id,
    )
    user_entry = db.exec(stmt).first()

    if not user_entry:
        return None

    # Get dictionary entry to extract meanings
    stmt = select(DictionaryEntry).where(DictionaryEntry.id == entry_id)
    entry = db.exec(stmt).first()
    if not entry:
        return None

    # Get all FSRS data for this entry
    stmt = select(MeaningFSRS).where(MeaningFSRS.dictionary_entry_id == entry_id)
    fsrs_records = db.exec(stmt).all()

    # Map FSRS records to meanings
    entry_data = cast(EntryDataDict, entry.json_data)
    meanings = entry_data.get("meanings", [])
    fsrs_data = []

    for i, meaning in enumerate(meanings):
        # Find corresponding FSRS record (by index order)
        if i < len(fsrs_records):
            fsrs = fsrs_records[i]
            fsrs_data.append(
                {
                    "meaning_fsrs_id": fsrs.id,
                    "meaning_local_id": meaning.get("local_id", ""),
                    "due": fsrs.due,
                    "stability": fsrs.stability,
                    "difficulty": fsrs.difficulty,
                    "state": FSRSCardState(fsrs.state),
                    "step": fsrs.step,
                    "last_review": fsrs.last_review,
                    "reps": fsrs.reps,
                    "lapses": fsrs.lapses,
                }
            )

    return fsrs_data


async def update_dictionary_entry(
    db: Session,
    auth_user_id: str,
    entry_id: str,
    entry: AiDictionaryEntry,
    translations: list[AiMeaningTranslation],
) -> bool:
    """Update a dictionary entry with new data.

    Args:
        db: Database session
        auth_user_id: ID of the requesting user
        entry_id: ID of the dictionary entry to update
        entry: Updated dictionary entry
        translations: Updated translations

    Returns:
        True if update succeeded, False if not authorized or not found

    Raises:
        ValueError: If validation fails
    """
    # Check if user has access to this entry
    stmt = select(UserDictionaryEntry).where(
        UserDictionaryEntry.auth_user_id == auth_user_id,
        UserDictionaryEntry.dictionary_entry_id == entry_id,
    )
    user_entry = db.exec(stmt).first()

    if not user_entry:
        return False

    # Validate that all meanings have translations
    meaning_ids = {meaning.local_id for meaning in entry.meanings}
    translation_meaning_ids = {trans.meaning_local_id for trans in translations}

    if meaning_ids != translation_meaning_ids:
        missing = meaning_ids - translation_meaning_ids
        extra = translation_meaning_ids - meaning_ids
        raise ValueError(
            f"Translation validation failed. Missing translations for: {missing}. "
            f"Extra translations for: {extra}."
        )

    # Update dictionary entry
    stmt = select(DictionaryEntry).where(DictionaryEntry.id == entry_id)
    dict_entry = db.exec(stmt).first()
    if not dict_entry:
        return False

    dict_entry.json_data = entry.model_dump()

    # Update translations
    stmt = select(DictionaryEntryTranslation).where(
        DictionaryEntryTranslation.dictionary_entry_id == entry_id
    )
    dict_translation = db.exec(stmt).first()

    if dict_translation:
        dict_translation.json_data = [trans.model_dump() for trans in translations]

    # Handle FSRS records - check if meanings changed
    stmt = select(MeaningFSRS).where(MeaningFSRS.dictionary_entry_id == entry_id)
    existing_fsrs = db.exec(stmt).all()

    # If number of meanings changed, we need to adjust FSRS records
    current_meanings_count = len(entry.meanings)
    existing_fsrs_count = len(existing_fsrs)

    if current_meanings_count > existing_fsrs_count:
        # Add new FSRS records for new meanings
        for _ in range(existing_fsrs_count, current_meanings_count):
            fsrs_data = new_training_data()
            meaning_fsrs = MeaningFSRS(
                id=generate_uuidv7(),
                dictionary_entry_id=entry_id,
                due=fsrs_data.due,
                stability=fsrs_data.stability,
                difficulty=fsrs_data.difficulty,
                state=fsrs_data.state,
                step=fsrs_data.step,
                last_review=fsrs_data.last_review,
                reps=fsrs_data.reps,
                lapses=fsrs_data.lapses,
            )
            db.add(meaning_fsrs)
    elif current_meanings_count < existing_fsrs_count:
        # Remove excess FSRS records
        for i in range(current_meanings_count, existing_fsrs_count):
            db.delete(existing_fsrs[i])

    db.commit()
    return True


def update_meaning_fsrs(
    db: Session,
    auth_user_id: str,
    entry_id: str,
    meaning_fsrs_id: str,
    rating: int,
    review_time: datetime,
) -> bool:
    """Update FSRS data for a meaning after review.

    Args:
        db: Database session
        auth_user_id: ID of the requesting user
        entry_id: ID of the dictionary entry
        meaning_fsrs_id: ID of the FSRS record to update
        rating: Review rating (1-4)
        review_time: When the review was performed

    Returns:
        True if update succeeded, False if not authorized or not found
    """
    # Check if user has access to this entry
    stmt = select(UserDictionaryEntry).where(
        UserDictionaryEntry.auth_user_id == auth_user_id,
        UserDictionaryEntry.dictionary_entry_id == entry_id,
    )
    user_entry = db.exec(stmt).first()

    if not user_entry:
        return False

    # Get the FSRS record
    stmt = select(MeaningFSRS).where(
        MeaningFSRS.id == meaning_fsrs_id,
        MeaningFSRS.dictionary_entry_id == entry_id,
    )
    meaning_fsrs = db.exec(stmt).first()

    if not meaning_fsrs:
        return False

    # Process the review
    current_data = FSRSTrainingData(
        due=meaning_fsrs.due,
        stability=meaning_fsrs.stability,
        difficulty=meaning_fsrs.difficulty,
        state=FSRSCardState(meaning_fsrs.state),
        step=meaning_fsrs.step,
        last_review=meaning_fsrs.last_review,
        reps=meaning_fsrs.reps,
        lapses=meaning_fsrs.lapses,
    )

    updated_data = process_review(current_data, Rating(rating), review_time)

    # Update the record
    meaning_fsrs.due = updated_data.due
    meaning_fsrs.stability = updated_data.stability
    meaning_fsrs.difficulty = updated_data.difficulty
    meaning_fsrs.state = updated_data.state
    meaning_fsrs.step = updated_data.step
    meaning_fsrs.last_review = updated_data.last_review
    meaning_fsrs.reps = updated_data.reps
    meaning_fsrs.lapses = updated_data.lapses

    db.commit()
    return True
