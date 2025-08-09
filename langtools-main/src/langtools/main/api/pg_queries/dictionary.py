"""Database queries for dictionary entries."""

import json
from datetime import datetime
from typing import Any, Optional

from langtools.ai import AiDictionaryEntry, AiMeaningTranslation
from sqlalchemy import func, select
from sqlmodel import Session

from ..models import DictionaryEntry, DictionaryEntryTranslation, RUserDictionaryEntry
from langtools.main.api.utils.id_generation import generate_pg_uuid


def _serialize_with_unicode(obj: dict[str, Any]) -> dict[str, Any]:  # type: ignore[misc]
    """Serialize dict to ensure proper Unicode handling."""
    # Convert to JSON string with Unicode preserved, then back to dict
    json_str = json.dumps(obj, ensure_ascii=False)
    return json.loads(json_str)  # type: ignore[no-any-return]


def find_latest_dictionary_entry_for_user(
    session: Session, auth_user_id: str, term: str, source_language: Optional[str] = None
) -> Optional[DictionaryEntry]:
    """Find the latest dictionary entry for a user's term and optionally source language."""
    # Build where clause step by step
    stmt = (
        select(DictionaryEntry)
        .join(RUserDictionaryEntry, DictionaryEntry.id == RUserDictionaryEntry.dictionary_entry_id)  # type: ignore[arg-type]
        .where(RUserDictionaryEntry.auth_user_id == auth_user_id)  # type: ignore[arg-type]
        .where(func.json_extract_path_text(DictionaryEntry.json_data, "headword") == term)  # type: ignore[arg-type]
    )

    # Add source_language condition if provided
    if source_language:
        stmt = stmt.where(
            func.json_extract_path_text(DictionaryEntry.json_data, "source_language")  # type: ignore[arg-type]
            == source_language
        )

    stmt = stmt.order_by(DictionaryEntry.updated_at.desc()).limit(1)  # type: ignore[attr-defined]
    result = session.exec(stmt)  # type: ignore[arg-type]
    return result.scalar_one_or_none()


def find_latest_translation_for_entry(
    session: Session, dictionary_entry_id: str, translation_language: str
) -> Optional[DictionaryEntryTranslation]:
    """Find the latest translation for a dictionary entry in a specific language."""
    stmt = (
        select(DictionaryEntryTranslation)
        .where(DictionaryEntryTranslation.dictionary_entry_id == dictionary_entry_id)  # type: ignore[arg-type]
        .where(DictionaryEntryTranslation.translation_language == translation_language)  # type: ignore[arg-type]
        .order_by(DictionaryEntryTranslation.updated_at.desc())  # type: ignore[attr-defined]
        .limit(1)
    )
    result = session.exec(stmt)  # type: ignore[arg-type]
    return result.scalar_one_or_none()


def create_dictionary_entry(
    session: Session, auth_user_id: str, ai_entry: AiDictionaryEntry
) -> DictionaryEntry:
    """Create a new dictionary entry and associate it with a user."""
    # Create the dictionary entry with proper Unicode serialization
    entry = DictionaryEntry(
        id=generate_pg_uuid(),
        json_data=_serialize_with_unicode(ai_entry.model_dump()),
    )
    session.add(entry)

    # Create the user association
    user_entry = RUserDictionaryEntry(
        id=generate_pg_uuid(),
        auth_user_id=auth_user_id,
        dictionary_entry_id=entry.id,
    )
    session.add(user_entry)

    session.flush()
    return entry


def create_dictionary_translation(
    session: Session,
    dictionary_entry_id: str,
    translation_language: str,
    translations: list[AiMeaningTranslation],
) -> DictionaryEntryTranslation:
    """Create a new translation for a dictionary entry."""
    # Serialize translations with proper Unicode handling
    translation_data = [_serialize_with_unicode(t.model_dump()) for t in translations]

    translation = DictionaryEntryTranslation(
        id=generate_pg_uuid(),
        dictionary_entry_id=dictionary_entry_id,
        translation_language=translation_language,
        json_data=translation_data,
    )
    session.add(translation)
    session.flush()
    return translation


def associate_user_with_dictionary_entry(
    session: Session, auth_user_id: str, dictionary_entry_id: str
) -> RUserDictionaryEntry:
    """Associate a user with an existing dictionary entry."""
    # Check if association already exists
    stmt = (
        select(RUserDictionaryEntry)
        .where(RUserDictionaryEntry.auth_user_id == auth_user_id)  # type: ignore[arg-type]
        .where(RUserDictionaryEntry.dictionary_entry_id == dictionary_entry_id)  # type: ignore[arg-type]
    )
    result = session.exec(stmt)  # type: ignore[arg-type]
    existing = result.scalar_one_or_none()

    if existing:
        # Update the updated_at timestamp
        existing.updated_at = datetime.now()
        return existing

    # Create new association
    user_entry = RUserDictionaryEntry(
        id=generate_pg_uuid(),
        auth_user_id=auth_user_id,
        dictionary_entry_id=dictionary_entry_id,
    )
    session.add(user_entry)
    session.flush()
    return user_entry
