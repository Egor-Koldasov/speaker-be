"""
Tests for MCP server functionality.
"""

from typing import Dict, List, Tuple, cast
from unittest.mock import AsyncMock, patch

from langtools.ai.models import (
    AiDictionaryEntry,
    AiMeaning,
    AiMeaningTranslation,
    DictionaryEntryParams,
    DictionaryWorkflowResult,
    ModelType,
)
from langtools.mcp.server import generate_dictionary_entry_tool


class TestMockMeaning:
    """Mock meaning object for tests."""

    def __init__(self, **kwargs: object):
        for key, value in kwargs.items():
            setattr(self, key, value)


class TestMockDictionaryEntry:
    """Mock dictionary entry for tests."""

    def __init__(self, **kwargs: object):
        for key, value in kwargs.items():
            setattr(self, key, value)


def create_meaning_from_dict(meaning_dict: Dict[str, object]) -> AiMeaning:
    """Helper to create Meaning from dict with proper field mapping."""
    return AiMeaning(
        headword=cast(str, meaning_dict.get("headword", "")),
        local_id=cast(str, meaning_dict.get("id", "")),
        canonical_form=cast(str, meaning_dict.get("canonical_form", "")),
        alternate_spellings=cast(list[str], meaning_dict.get("alternate_spellings", [])),
        definition=cast(str, meaning_dict.get("definition", "")),
        part_of_speech=cast(str, meaning_dict.get("part_of_speech", "")),
        morphology=cast(str, meaning_dict.get("morphology", "")),
        register=cast(str, meaning_dict.get("register", "")),
        frequency=cast(str, meaning_dict.get("frequency", "")),
        etymology=cast(str, meaning_dict.get("etymology", "")),
        difficulty_level=cast(str, meaning_dict.get("difficulty_level", "")),
        learning_priority=cast(str, meaning_dict.get("learning_priority", "")),
        pronunciation=cast(str, meaning_dict.get("pronunciation", "")),
        example_sentences=cast(list[str], meaning_dict.get("example_sentences", [])),
    )


class TestGenerateDictionaryEntryTool:
    """Test cases for generate_dictionary_entry_tool."""

    @patch("langtools.mcp.server.generate_dictionary_workflow")
    async def test_successful_generation(self, mock_generate: AsyncMock) -> None:
        """Test successful dictionary entry generation via MCP tool."""
        # Mock the workflow result
        base_entry = AiDictionaryEntry(
            headword="сырой",
            source_language="ru",
            meanings=[
                create_meaning_from_dict(
                    {
                        "headword": "сырой",
                        "id": "сырой-0",
                        "canonical_form": "сырой",
                        "alternate_spellings": [],
                        "definition": "Не подвергшийся тепловой обработке",
                        "part_of_speech": "прилагательное",
                        "morphology": "качественное прилагательное",
                        "register": "нейтральный",
                        "frequency": "common",
                        "etymology": "от праславянского *syrъ",
                        "difficulty_level": "intermediate",
                        "learning_priority": "high",
                        "pronunciation": "ˈsɨrəj",
                        "example_sentences": ["Сырое мясо", "Сырые овощи"],
                    }
                )
            ],
        )

        translations = [
            AiMeaningTranslation(
                meaning_local_id="сырой-0",
                headword="raw",
                canonical_form="raw",
                translation_language="en",
                translation="raw, uncooked",
                definition="Not subjected to heat treatment",
                part_of_speech="adjective",
                morphology="descriptive adjective",
                register="neutral",
                frequency="common",
                etymology="from Proto-Slavic *syrъ",
                difficulty_level="intermediate",
                learning_priority="high",
                pronunciation="rɔː",
                pronunciation_tips="Pronounced like 'raw' in English",
                example_sentences_translations=["Raw meat", "Raw vegetables"],
            )
        ]

        workflow_result = DictionaryWorkflowResult(
            entry=base_entry,
            translations=translations,
        )

        mock_generate.return_value = workflow_result

        # Call the MCP tool
        result = await generate_dictionary_entry_tool(
            translating_term="сырой",
            user_learning_languages="en:1,ru:2",
            translation_language="en",
            model="claude-sonnet-4-0",
        )

        # Verify result structure
        assert isinstance(result, dict)
        assert "entry" in result
        assert "translations" in result

        # Verify entry data
        entry_data = cast(Dict[str, object], result["entry"])
        assert cast(str, entry_data["source_language"]) == "ru"
        assert cast(str, entry_data["headword"]) == "сырой"
        meanings_list = cast(List[Dict[str, object]], entry_data["meanings"])
        assert len(meanings_list) == 1

        meaning = meanings_list[0]
        assert cast(str, meaning["canonical_form"]) == "сырой"
        assert cast(str, meaning["id"]) == "сырой-0"

        # Verify translations data
        translation_data = cast(List[Dict[str, object]], result["translations"])
        assert len(translation_data) == 1
        assert cast(str, translation_data[0]["meaning_id"]) == "сырой-0"
        assert cast(str, translation_data[0]["translation"]) == "raw, uncooked"

        # Verify function was called with correct parameters
        mock_generate.assert_called_once()
        call_args = cast(Tuple[object, ...], mock_generate.call_args[0])
        params = cast(DictionaryEntryParams, call_args[0])
        model_type = cast(ModelType, call_args[1])

        assert isinstance(params, DictionaryEntryParams)
        assert params.translating_term == "сырой"
        assert params.user_learning_languages == "en:1,ru:2"
        assert params.translation_language == "en"
        assert model_type == ModelType.CLAUDE_SONNET_4

    @patch("langtools.mcp.server.generate_dictionary_workflow")
    async def test_english_generation(self, mock_generate: AsyncMock) -> None:
        """Test English word dictionary generation."""
        # Mock the workflow result for English
        base_entry = AiDictionaryEntry(
            headword="hello",
            source_language="en",
            meanings=[
                create_meaning_from_dict(
                    {
                        "headword": "hello",
                        "id": "hello-0",
                        "canonical_form": "hello",
                        "alternate_spellings": [],
                        "definition": "A greeting",
                        "part_of_speech": "interjection",
                        "morphology": "interjection",
                        "register": "neutral",
                        "frequency": "very_common",
                        "etymology": "from Old English hello",
                        "difficulty_level": "beginner",
                        "learning_priority": "essential",
                        "pronunciation": "həˈloʊ",
                        "example_sentences": ["Hello, how are you?", "Say hello to your friend"],
                    }
                )
            ],
        )

        translations = [
            AiMeaningTranslation(
                meaning_local_id="hello-0",
                headword="привет",
                canonical_form="привет",
                translation_language="ru",
                translation="привет, здравствуйте",
                definition="Приветствие",
                part_of_speech="междометие",
                morphology="междометие",
                register="нейтральный",
                frequency="очень_часто",
                etymology="от английского hello",
                difficulty_level="начальный",
                learning_priority="важный",
                pronunciation="prʲɪˈvʲet",
                pronunciation_tips="Stressed on the second syllable",
                example_sentences_translations=["Привет, как дела?", "Скажи привет своему другу"],
            )
        ]

        workflow_result = DictionaryWorkflowResult(
            entry=base_entry,
            translations=translations,
        )

        mock_generate.return_value = workflow_result

        # Call the MCP tool for English to Russian
        result = await generate_dictionary_entry_tool(
            translating_term="hello",
            user_learning_languages="ru:2,en:1",
            translation_language="ru",
            model="claude-sonnet-4-0",
        )

        # Verify result structure
        assert isinstance(result, dict)
        entry_dict = cast(Dict[str, object], result["entry"])
        assert cast(str, entry_dict["source_language"]) == "en"
        assert cast(str, entry_dict["headword"]) == "hello"

        meaning = cast(List[Dict[str, object]], entry_dict["meanings"])[0]
        assert cast(str, meaning["canonical_form"]) == "hello"

        # Verify Russian translation
        translation = cast(List[Dict[str, object]], result["translations"])[0]
        assert cast(str, translation["translation_language"]) == "ru"
        assert cast(str, translation["translation"]) == "привет, здравствуйте"

    @patch("langtools.mcp.server.generate_dictionary_workflow")
    async def test_invalid_model_defaults_to_claude(self, mock_generate: AsyncMock) -> None:
        """Test that invalid model parameter defaults to Claude Sonnet."""
        # Mock workflow result
        base_entry = AiDictionaryEntry(
            headword="test",
            source_language="en",
            meanings=[
                create_meaning_from_dict(
                    {
                        "headword": "test",
                        "id": "test-0",
                        "canonical_form": "test",
                        "alternate_spellings": [],
                        "definition": "a test",
                        "part_of_speech": "noun",
                        "morphology": "noun",
                        "register": "neutral",
                        "frequency": "common",
                        "etymology": "test",
                        "difficulty_level": "beginner",
                        "learning_priority": "medium",
                        "pronunciation": "test",
                        "example_sentences": ["This is a test", "Test example"],
                    }
                )
            ],
        )

        workflow_result = DictionaryWorkflowResult(
            entry=base_entry,
            translations=[],
        )

        mock_generate.return_value = workflow_result

        # Call with invalid model
        await generate_dictionary_entry_tool(
            translating_term="test",
            user_learning_languages="en:1",
            translation_language="es",
            model="invalid-model",
        )

        # Verify default model was used
        call_args = cast(Tuple[object, ...], mock_generate.call_args[0])
        model_type = cast(ModelType, call_args[1])
        assert model_type == ModelType.CLAUDE_SONNET_4  # Should default to CLAUDE_SONNET_4
