"""
Data models and types for AI functions.
"""

from __future__ import annotations

from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field


class ModelType(Enum):
    """Supported LLM model types."""

    GPT4 = "gpt-4"
    GPT3_5 = "gpt-3.5-turbo"
    GTP4_1_MINI = "gpt-4.1-mini-2025-04-14"
    GTP4_O_MINI = "gpt-4o-mini-2024-07-18"
    CLAUDE_SONNET_3_5 = "claude-3-5-haiku-latest"
    CLAUDE_SONNET_4 = "claude-sonnet-4-0"


class DictionaryEntryParams(BaseModel):
    """Input parameters for dictionary entry generation."""

    translating_term: str = Field(description="The word or phrase to define and translate")
    user_learning_languages: str = Field(
        description="User's language preferences in format 'en:1,ru:2'"
    )
    translation_language: str = Field(
        description="Target language for translations in BCP 47 format"
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "translating_term": "сырой",
                "user_learning_languages": "en:1,ru:2",
                "translation_language": "en",
            }
        }
    }


class Meaning(BaseModel):
    """A single meaning of a dictionary entry."""

    headword: str = Field(
        description="Word form as users encounter it (can be inflected, variant spelling, etc.)"
    )
    id: str = Field(
        description="Unique identifier for the meaning in format {headword}-{index} starting from 1"
    )
    canonical_form: str = Field(
        description="Standard dictionary form - base/citation form (infinitive, nominative, etc.)"
    )
    alternate_spellings: List[str] = Field(description="Other valid spellings or representations")
    definition: str = Field(description="Clear, comprehensive definition in original language")
    part_of_speech: str = Field(description="Part of speech in original language")
    semantic_field: Optional[str] = Field(
        default=None, description="Semantic domain (medicine, technology, sports, etc.)"
    )
    pronunciation: str = Field(description="Comma separated list of pronunciations in IPA format")
    tone_notation: Optional[str] = Field(
        default=None, description="Tone markers (Mandarin: xuéxí, Vietnamese: học tập)"
    )
    syllable_count: Optional[int] = Field(default=None, description="Number of syllables")
    phonetic_variations: Optional[List[str]] = Field(
        default=None, description="Regional pronunciation variants"
    )
    morphology: str = Field(description="The list of all the morphological features")
    register: str = Field(
        description="Formality level: formal, informal, colloquial, archaic, technical, vulgar"
    )
    frequency: str = Field(
        description="Usage frequency: very common, common, uncommon, rare, archaic"
    )
    etymology: str = Field(description="A detailed explanation of the word's etymology")
    difficulty_level: str = Field(
        description="Difficulty: beginner, elementary, intermediate, upper intermediate, advanced"
    )
    learning_priority: str = Field(description="Learning priority: essential, high, medium, low")
    common_mistakes: Optional[List[str]] = Field(default=None, description="Typical learner errors")
    mnemonic_hints: Optional[List[str]] = Field(
        default=None, description="Memory aids and mnemonics"
    )
    practice_suggestions: Optional[List[str]] = Field(
        default=None, description="Suggested practice methods"
    )

    example_sentences: List[str] = Field(
        description="3-5 example sentences in original language", min_length=2, max_length=5
    )
    collocations: Optional[List[str]] = Field(default=None, description="Common word combinations")
    synonyms: Optional[List[str]] = Field(default=None, description="Synonyms in original language")
    antonyms: Optional[List[str]] = Field(default=None, description="Antonyms in original language")


class BaseDictionaryParams(BaseModel):
    """Input parameters for base dictionary entry generation (step 1 of workflow)."""

    translating_term: str = Field(description="The word or phrase to define")
    user_learning_languages: str = Field(
        description="User's language preferences in format 'en:1,ru:2'"
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "translating_term": "сырой",
                "user_learning_languages": "en:1,ru:2",
            }
        }
    }


class TranslationParams(BaseModel):
    """Input parameters for meaning translations generation (step 2 of workflow)."""

    entry: AiDictionaryEntry = Field(description="Base dictionary entry to translate")
    translation_language: str = Field(
        description="Target language for translations in BCP 47 format"
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "translation_language": "en",
            }
        }
    }


class MeaningTranslationList(BaseModel):
    """Wrapper for list of meaning translations to work with LangChain structured output."""

    translations: List[MeaningTranslation] = Field(description="List of meaning translations")


class DictionaryWorkflowResult(BaseModel):
    """Complete result from dictionary workflow with base entry and translations."""

    entry: AiDictionaryEntry = Field(description="Base dictionary entry")
    translations: List[MeaningTranslation] = Field(description="Translations for all meanings")


class AiDictionaryEntry(BaseModel):
    """Complete dictionary entry with multiple meanings and metadata."""

    headword: str = Field(
        description="Word form as users encounter it (can be inflected, variant spelling, etc.)"
    )

    source_language: str = Field(
        description="Original language in BCP 47 format, guessed from word and user preferences"
    )
    meanings: list[Meaning] = Field(
        description="List of all meanings/senses ordered from most to least common usage",
        min_length=1,
    )


class MeaningTranslation(BaseModel):
    """Translation of `Meaning`."""

    meaning_id: str = Field(description="Meaning.id of the original meaning")

    headword: str = Field(
        description="Word form as users encounter it (can be inflected, variant spelling, etc.)"
    )
    canonical_form: str = Field(
        description="Standard dictionary form - base/citation form (infinitive, nominative, etc.)"
    )
    translation_language: str = Field(description="Translation language in BCP 47 format")

    translation: str = Field(
        description="Translation to target language, multiple words separated by comma"
    )
    definition: str = Field(description="Clear, comprehensive definition")
    part_of_speech: str = Field(description="Part of speech")
    semantic_field: Optional[str] = Field(
        default=None, description="Semantic domain (medicine, technology, sports, etc.)"
    )
    pronunciation: str = Field(description="Comma separated list of pronunciations in IPA format")
    pronunciation_tips: str = Field(
        description="Pronunciation tips in translation language in beginner-friendly way"
    )
    tone_notation: Optional[str] = Field(
        default=None, description="Tone markers (Mandarin: xuéxí, Vietnamese: học tập)"
    )
    tone_tips: Optional[str] = Field(
        default=None,
        description=(
            "Include for tonal languages: tone tips in translation language "
            "in beginner-friendly way"
        ),
    )
    morphology: str = Field(description="The list of all the morphological features")
    register: str = Field(
        description="Formality level: formal, informal, colloquial, archaic, technical, vulgar"
    )
    frequency: str = Field(
        description="Usage frequency: very common, common, uncommon, rare, archaic"
    )
    etymology: str = Field(description="Word's etymology")
    difficulty_level: str = Field(
        description="Difficulty: beginner, elementary, intermediate, upper intermediate, advanced"
    )
    learning_priority: str = Field(description="Learning priority: essential, high, medium, low")
    common_mistakes: Optional[List[str]] = Field(default=None, description="Typical learner errors")
    mnemonic_hints: Optional[List[str]] = Field(
        default=None, description="Memory aids and mnemonics"
    )
    practice_suggestions: Optional[List[str]] = Field(
        default=None, description="Suggested practice methods"
    )
    example_sentences_translations: List[str] = Field(
        description="Translations of the original meaning's examples", min_length=2, max_length=5
    )
    collocations: Optional[List[str]] = Field(
        default=None, description="Translations of the original meaning's common word combinations"
    )
