"""Dictionary entry database queries using SQLModel."""

from typing import List
from sqlmodel import select

from ..database import get_session
from ..models.dictionary_entry import DictionaryEntry
from ..models.r_user_dictionary_entry import RUserDictionaryEntry
from ..models.dictionary_entry_translation import DictionaryEntryTranslation
from ..models.fsrs import FSRS
from ..models.r_meaning_translation_fsrs import RMeaningTranslationFsrs
from ..utils import generate_pg_uuid
from langtools.ai.models import DictionaryWorkflowResult, AiMeaningTranslation
from langtools.main.fsrs.models import FSRSTrainingData, FSRSCardState
from datetime import datetime


class DictionaryEntryError(Exception):
    """Base exception for dictionary entry operations."""


class InvalidMeaningTranslationError(DictionaryEntryError):
    """Raised when meaning translations have invalid meaning_local_id fields."""


def create_dictionary_entry_with_fsrs(
    auth_user_id: str, workflow_result: DictionaryWorkflowResult
) -> DictionaryEntry:
    """
    Create a complete dictionary entry with translations and FSRS data.

    Args:
        auth_user_id: User ID to associate with the dictionary entry
        workflow_result: Complete dictionary workflow result with entry and translations

    Returns:
        Created DictionaryEntry model

    Raises:
        InvalidMeaningTranslationError: If translations don't have proper meaning_local_id fields
        IntegrityError: If database constraints are violated
    """
    with get_session() as session:
        try:
            # Validate that all meanings have corresponding translations
            entry_meaning_ids = {meaning.local_id for meaning in workflow_result.entry.meanings}
            translation_meaning_ids = {
                trans.meaning_local_id for trans in workflow_result.translations
            }

            if entry_meaning_ids != translation_meaning_ids:
                raise InvalidMeaningTranslationError(
                    f"Meaning IDs mismatch: entry has {entry_meaning_ids}, "
                    + f"translations have {translation_meaning_ids}"
                )

            # Create dictionary entry
            dictionary_entry_id = generate_pg_uuid()
            dictionary_entry = DictionaryEntry(
                id=dictionary_entry_id, json_data=workflow_result.entry.model_dump()
            )
            session.add(dictionary_entry)

            # Create user-dictionary entry relationship
            user_dict_entry_id = generate_pg_uuid()
            user_dict_entry = RUserDictionaryEntry(
                id=user_dict_entry_id,
                auth_user_id=auth_user_id,
                dictionary_entry_id=dictionary_entry_id,
            )
            session.add(user_dict_entry)

            # Group translations by language
            translations_by_lang: dict[str, List[AiMeaningTranslation]] = {}
            for translation in workflow_result.translations:
                lang = translation.translation_language
                if lang not in translations_by_lang:
                    translations_by_lang[lang] = []
                translations_by_lang[lang].append(translation)

            # Create dictionary entry translations for each language
            for translation_language, translations in translations_by_lang.items():
                dict_entry_trans_id = generate_pg_uuid()
                dict_entry_translation = DictionaryEntryTranslation(
                    id=dict_entry_trans_id,
                    dictionary_entry_id=dictionary_entry_id,
                    translation_language=translation_language,
                    json_data=[trans.model_dump() for trans in translations],
                )
                session.add(dict_entry_translation)

                # Create FSRS records for each meaning translation
                for translation in translations:
                    # Create initial FSRS training data (new card)
                    fsrs_id = generate_pg_uuid()
                    initial_fsrs = FSRSTrainingData(
                        due=datetime.now(),  # Due immediately for new cards
                        stability=None,  # No stability for new cards
                        difficulty=None,  # No difficulty for new cards
                        state=FSRSCardState.LEARNING,
                        step=0,  # First learning step
                        last_review=None,  # Never reviewed
                        reps=0,  # No reviews yet
                        lapses=0,  # No lapses yet
                    )

                    fsrs_record = FSRS(
                        id=fsrs_id,
                        due=initial_fsrs.due,
                        stability=initial_fsrs.stability,
                        difficulty=initial_fsrs.difficulty,
                        state=initial_fsrs.state,
                        step=initial_fsrs.step,
                        last_review=initial_fsrs.last_review,
                        reps=initial_fsrs.reps,
                        lapses=initial_fsrs.lapses,
                    )
                    session.add(fsrs_record)

                    # Link FSRS record to the meaning translation
                    meaning_fsrs_id = generate_pg_uuid()
                    meaning_fsrs = RMeaningTranslationFsrs(
                        id=meaning_fsrs_id,
                        dictionary_entry_translation_id=dict_entry_trans_id,
                        meaning_local_id=translation.meaning_local_id,
                        fsrs_id=fsrs_id,
                    )
                    session.add(meaning_fsrs)

            # Commit all changes
            session.commit()
            session.refresh(dictionary_entry)

            return dictionary_entry

        except Exception as e:
            session.rollback()
            raise e


def get_user_dictionary_entries(auth_user_id: str) -> List[DictionaryEntry]:
    """
    Get all dictionary entries for a user.

    Args:
        auth_user_id: User ID

    Returns:
        List of DictionaryEntry models
    """
    with get_session() as session:
        statement = (
            select(DictionaryEntry)
            .join(RUserDictionaryEntry)
            .where(RUserDictionaryEntry.auth_user_id == auth_user_id)
        )
        return list(session.exec(statement).all())
