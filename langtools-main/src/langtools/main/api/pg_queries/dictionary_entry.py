"""Database query functions for dictionary entries."""

from typing import Optional
from sqlmodel import Session, select, desc
from langtools.ai import AiDictionaryEntry, AiMeaningTranslation

from ..models import DictionaryEntry, DictionaryEntryTranslation, RUserDictionaryEntry
from ..utils.id_generation import generate_pg_uuid


async def find_dictionary_entry_by_term(
    session: Session,
    term: str,
    auth_user_id: Optional[str] = None,
) -> Optional[DictionaryEntry]:
    """Find the most recent dictionary entry for a term (any source language).

    Args:
        session: Database session
        term: The term to search for
        auth_user_id: ID of the authenticated user (optional)

    Returns:
        Most recent DictionaryEntry or None if not found
    """
    statement = select(DictionaryEntry).where(
        DictionaryEntry.json_data["headword"].as_string() == term,  # type: ignore[attr-defined]
    )

    # Filter by user association if user is authenticated
    if auth_user_id:
        statement = statement.join(
            RUserDictionaryEntry, RUserDictionaryEntry.dictionary_entry_id == DictionaryEntry.id
        ).where(RUserDictionaryEntry.auth_user_id == auth_user_id)

    statement = statement.order_by(desc(DictionaryEntry.updated_at))
    return session.exec(statement).first()


async def find_dictionary_entry_translations(
    session: Session,
    dictionary_entry_id: str,
    translation_language: str,
    auth_user_id: Optional[str] = None,
) -> Optional[DictionaryEntryTranslation]:
    """Find the most recent translations for a dictionary entry and language.

    Args:
        session: Database session
        dictionary_entry_id: ID of the dictionary entry
        translation_language: Target translation language
        auth_user_id: ID of the authenticated user (optional)

    Returns:
        Most recent DictionaryEntryTranslation or None if not found
    """
    statement = select(DictionaryEntryTranslation).where(
        DictionaryEntryTranslation.dictionary_entry_id == dictionary_entry_id,
        DictionaryEntryTranslation.translation_language == translation_language,
    )

    # Filter by user association if user is authenticated
    if auth_user_id:
        statement = (
            statement.join(
                DictionaryEntry,
                DictionaryEntry.id == DictionaryEntryTranslation.dictionary_entry_id,
            )
            .join(
                RUserDictionaryEntry, RUserDictionaryEntry.dictionary_entry_id == DictionaryEntry.id
            )
            .where(RUserDictionaryEntry.auth_user_id == auth_user_id)
        )

    statement = statement.order_by(desc(DictionaryEntryTranslation.updated_at))
    return session.exec(statement).first()


async def create_dictionary_entry(
    session: Session,
    ai_entry: AiDictionaryEntry,
) -> DictionaryEntry:
    """Create a new dictionary entry.

    Args:
        session: Database session
        ai_entry: AI-generated dictionary entry data

    Returns:
        Created DictionaryEntry
    """
    # Use direct model_dump to avoid JSON serialization issues
    dictionary_entry = DictionaryEntry(
        id=generate_pg_uuid(),
        json_data=ai_entry.model_dump(mode="python"),
    )

    session.add(dictionary_entry)
    session.commit()
    session.refresh(dictionary_entry)

    return dictionary_entry


async def create_dictionary_entry_translations(
    session: Session,
    dictionary_entry_id: str,
    translation_language: str,
    translations: list[AiMeaningTranslation],
) -> DictionaryEntryTranslation:
    """Create translations for a dictionary entry.

    Args:
        session: Database session
        dictionary_entry_id: ID of the dictionary entry
        translation_language: Target translation language
        translations: List of meaning translations

    Returns:
        Created DictionaryEntryTranslation
    """
    # Use direct model_dump to avoid JSON serialization issues
    translations_data = [t.model_dump(mode="python") for t in translations]
    entry_translation = DictionaryEntryTranslation(
        id=generate_pg_uuid(),
        dictionary_entry_id=dictionary_entry_id,
        translation_language=translation_language,
        json_data=translations_data,  # type: ignore[arg-type]
    )

    session.add(entry_translation)
    session.commit()
    session.refresh(entry_translation)

    return entry_translation


async def create_user_dictionary_entry_relation(
    session: Session,
    auth_user_id: str,
    dictionary_entry_id: str,
) -> RUserDictionaryEntry:
    """Create a relation between user and dictionary entry.

    Args:
        session: Database session
        auth_user_id: ID of the authenticated user
        dictionary_entry_id: ID of the dictionary entry

    Returns:
        Created RUserDictionaryEntry
    """
    # Check if relation already exists
    statement = select(RUserDictionaryEntry).where(
        RUserDictionaryEntry.auth_user_id == auth_user_id,
        RUserDictionaryEntry.dictionary_entry_id == dictionary_entry_id,
    )
    existing = session.exec(statement).first()

    if existing:
        return existing

    relation = RUserDictionaryEntry(
        id=generate_pg_uuid(),
        auth_user_id=auth_user_id,
        dictionary_entry_id=dictionary_entry_id,
    )

    session.add(relation)
    session.commit()
    session.refresh(relation)

    return relation


async def validate_translations_completeness(
    entry: AiDictionaryEntry,
    translations: list[AiMeaningTranslation],
) -> bool:
    """Validate that all meanings have corresponding translations.

    Args:
        entry: Dictionary entry with meanings
        translations: List of translations

    Returns:
        True if all meanings have translations with matching local_ids
    """
    meaning_ids = {meaning.local_id for meaning in entry.meanings}
    translation_ids = {translation.meaning_local_id for translation in translations}

    return meaning_ids == translation_ids
