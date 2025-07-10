"""
Data models and types for AI functions.
"""

from enum import Enum

from pydantic import BaseModel, Field


class ModelType(Enum):
    """Supported LLM model types."""

    GPT4 = "gpt-4"
    GPT3_5 = "gpt-3.5-turbo"
    CLAUDE_SONNET = "claude-3-5-sonnet-20241022"
    CLAUDE_SONNET_4 = "claude-sonnet-4-0"


class DictionaryEntryParams(BaseModel):
    """Input parameters for dictionary entry generation (matches Go experiment structure)."""

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

    id: str = Field(description="Unique identifier for the meaning in format {neutralForm}-{index}")
    neutral_form: str = Field(
        description="The word in a neutral grammatic form of the original language"
    )
    definition_original: str = Field(
        description="A detailed definition of the word in the original language"
    )
    definition_translated: str = Field(
        description="A detailed definition of the word in the target language"
    )
    translation: str = Field(
        description="Translation to target language, multiple words separated by comma"
    )
    pronunciation: str = Field(description="Comma separated list of pronunciations in IPA format")
    synonyms: str = Field(description="Common synonyms in the original language")


class AiDictionaryEntry(BaseModel):
    """Complete dictionary entry with multiple meanings and metadata."""

    source_language: str = Field(
        description="Original language in BCP 47 format, guessed from word and user preferences"
    )
    meanings: list[Meaning] = Field(
        description="List of all meanings ordered from most to least common usage",
        min_length=1,
    )

    # class Config:
    #     json_schema_extra = {
    #         "example": {
    #             "source_language": "ru",
    #             "meanings": [
    #                 {
    #                     "id": "сырой-0",
    #                     "neutral_form": "сырой",
    #                     "definition_original": "Не подвергшийся тепловой обработке; необработанный, неприготовленный (о пище)",
    #                     "definition_translated": "Not subjected to heat treatment; unprocessed, uncooked (referring to food)",
    #                     "translation": "raw, uncooked, fresh",
    #                     "pronunciation": "ˈsɨrəj",
    #                     "synonyms": "необработанный, неприготовленный, свежий"
    #                 },
    #                 {
    #                     "id": "сырой-1",
    #                     "neutral_form": "сырой",
    #                     "definition_original": "Содержащий влагу, не высохший; влажный, мокрый",
    #                     "definition_translated": "Containing moisture, not dried; damp, wet",
    #                     "translation": "damp, wet, moist, humid",
    #                     "pronunciation": "ˈsɨrəj",
    #                     "synonyms": "влажный, мокрый, промокший, непросохший"
    #                 },
    #                 {
    #                     "id": "сырой-2",
    #                     "neutral_form": "сырой",
    #                     "definition_original": "Необработанный, неочищенный; в первоначальном виде (о материалах, продукции)",
    #                     "definition_translated": "Unprocessed, unrefined; in original form (referring to materials, products)",
    #                     "translation": "crude, raw, unrefined, unprocessed",
    #                     "pronunciation": "ˈsɨrəj",
    #                     "synonyms": "необработанный, неочищенный, первичный"
    #                 },
    #                 {
    #                     "id": "сырой-3",
    #                     "neutral_form": "сырой",
    #                     "definition_original": "Неопытный, неподготовленный; недостаточно развитый (разговорное)",
    #                     "definition_translated": "Inexperienced, unprepared; insufficiently developed (colloquial)",
    #                     "translation": "green, inexperienced, raw, undeveloped",
    #                     "pronunciation": "ˈsɨrəj",
    #                     "synonyms": "неопытный, неподготовленный, незрелый"
    #                 }
    #             ]
    #         }
    #     }
