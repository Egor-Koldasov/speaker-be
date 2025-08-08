"""Database queries for dictionary entries."""

from sqlmodel import Session

from langtools.ai.models import AiDictionaryEntry, AiMeaningTranslation
from langtools.main.api.models import (
    DictionaryEntry,
    DictionaryEntryTranslation,
    MeaningFSRS,
    UserDictionaryEntry,
)
from langtools.main.api.utils.id_generation import generate_uuidv7
from langtools.main.fsrs.functions import new_training_data


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
            f"Translation validation failed. "
            f"Missing translations for: {missing}. "
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
