"""
Tests for MCP server functionality.
"""

import json
from unittest.mock import AsyncMock, patch

import pytest

from langtools.ai.models import (
    AiDictionaryEntry,
    DictionaryEntryParams,
    DictionaryWorkflowResult,
    Meaning,
    MeaningTranslation,
    ModelType,
)
from langtools.mcp.server import generate_dictionary_entry_tool


class TestMockMeaning:
    """Mock meaning object for tests."""

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


class TestMockDictionaryEntry:
    """Mock dictionary entry for tests."""

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


def create_meaning_from_dict(meaning_dict: dict) -> Meaning:
    """Helper to create Meaning from dict with proper field mapping."""
    return Meaning(
        headword=meaning_dict.get("headword", ""),
        id=meaning_dict.get("id", ""),
        canonical_form=meaning_dict.get("canonical_form", ""),
        alternate_spellings=meaning_dict.get("alternate_spellings", []),
        definition=meaning_dict.get("definition", ""),
        part_of_speech=meaning_dict.get("part_of_speech", ""),
        morphology=meaning_dict.get("morphology", ""),
        register=meaning_dict.get("register", ""),
        frequency=meaning_dict.get("frequency", ""),
        etymology=meaning_dict.get("etymology", ""),
        difficulty_level=meaning_dict.get("difficulty_level", ""),
        learning_priority=meaning_dict.get("learning_priority", ""),
        pronunciation=meaning_dict.get("pronunciation", ""),
        example_sentences=meaning_dict.get("example_sentences", []),
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
                create_meaning_from_dict({
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
                })
            ],
        )

        translations = [
            MeaningTranslation(
                meaning_id="сырой-0",
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
        entry_data = result["entry"]
        assert entry_data["source_language"] == "ru"
        assert entry_data["headword"] == "сырой"
        assert len(entry_data["meanings"]) == 1
        
        meaning = entry_data["meanings"][0]
        assert meaning["canonical_form"] == "сырой"
        assert meaning["id"] == "сырой-0"

        # Verify translations data
        translation_data = result["translations"]
        assert len(translation_data) == 1
        assert translation_data[0]["meaning_id"] == "сырой-0"
        assert translation_data[0]["translation"] == "raw, uncooked"

        # Verify function was called with correct parameters
        mock_generate.assert_called_once()
        call_args = mock_generate.call_args[0]
        params = call_args[0]
        model_type = call_args[1]

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
                create_meaning_from_dict({
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
                })
            ],
        )

        translations = [
            MeaningTranslation(
                meaning_id="hello-0",
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
        assert result["entry"]["source_language"] == "en"
        assert result["entry"]["headword"] == "hello"
        
        meaning = result["entry"]["meanings"][0]
        assert meaning["canonical_form"] == "hello"

        # Verify Russian translation
        translation = result["translations"][0]
        assert translation["translation_language"] == "ru"
        assert translation["translation"] == "привет, здравствуйте"

    @patch("langtools.mcp.server.generate_dictionary_workflow")
    async def test_invalid_model_defaults_to_claude(self, mock_generate: AsyncMock) -> None:
        """Test that invalid model parameter defaults to Claude Sonnet."""
        # Mock workflow result
        base_entry = AiDictionaryEntry(
            headword="test",
            source_language="en",
            meanings=[
                create_meaning_from_dict({
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
                })
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
        call_args = mock_generate.call_args[0]
        model_type = call_args[1]
        assert model_type == ModelType.CLAUDE_SONNET  # Should default to CLAUDE_SONNET