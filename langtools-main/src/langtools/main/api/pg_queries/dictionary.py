"""Database queries for dictionary entries."""

import json
from datetime import datetime
from typing import Any, Optional

from sqlalchemy import func, select
from sqlmodel import Session

from langtools.ai import AiDictionaryEntry
from langtools.main.api.utils.id_generation import generate_pg_uuid

from ..models import DictionaryEntry, RUserDictionaryEntry


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


def get_dictionary_entry_by_id(session: Session, entry_id: str) -> DictionaryEntry:
    """Get a dictionary entry by its ID."""
    stmt = select(DictionaryEntry).where(DictionaryEntry.id == entry_id)  # type: ignore[arg-type]
    result = session.exec(stmt)  # type: ignore[arg-type]
    entry = result.scalar_one_or_none()
    if not entry:
        raise ValueError(f"Dictionary entry with id {entry_id} not found")
    return entry


def get_user_dictionary_entry_association(
    session: Session, auth_user_id: str, dictionary_entry_id: str
) -> RUserDictionaryEntry:
    """Get the user-dictionary entry association by user and entry IDs."""
    stmt = (
        select(RUserDictionaryEntry)
        .where(RUserDictionaryEntry.auth_user_id == auth_user_id)  # type: ignore[arg-type]
        .where(RUserDictionaryEntry.dictionary_entry_id == dictionary_entry_id)  # type: ignore[arg-type]
    )
    result = session.exec(stmt)  # type: ignore[arg-type]
    association = result.scalar_one_or_none()
    if not association:
        raise ValueError(
            f"User-dictionary entry association not found for user {auth_user_id} "
            f"and entry {dictionary_entry_id}"
        )
    return association
