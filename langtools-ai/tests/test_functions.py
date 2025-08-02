"""
Tests for AI functions.
"""

from unittest.mock import AsyncMock, Mock, patch

import pytest

from langtools.ai.functions import (
    ValidationError,
    generate_base_dictionary_entry,
    generate_dictionary_entry,
    generate_dictionary_workflow,
    generate_meaning_translations,
)
from langtools.ai.models import (
    AiDictionaryEntry,
    BaseDictionaryParams,
    DictionaryEntryParams,
    DictionaryWorkflowResult,
    Meaning,
    MeaningTranslation,
    ModelType,
    TranslationParams,
)


class TestGenerateBaseDictionaryEntry:
    """Test cases for generate_base_dictionary_entry function."""

    async def test_validate_empty_translating_term(self) -> None:
        """Test validation fails for empty translating term."""
        params = BaseDictionaryParams(translating_term="", user_learning_languages="en:1,ru:2")

        with pytest.raises(ValidationError, match="Translating term cannot be empty"):
            await generate_base_dictionary_entry(params, ModelType.CLAUDE_SONNET_4)

    async def test_validate_long_translating_term(self) -> None:
        """Test validation fails for overly long translating term."""
        params = BaseDictionaryParams(
            translating_term="a" * 101,  # 101 characters
            user_learning_languages="en:1,ru:2",
        )

        with pytest.raises(ValidationError, match="Translating term too long"):
            await generate_base_dictionary_entry(params, ModelType.CLAUDE_SONNET_4)

    async def test_validate_invalid_user_learning_languages(self) -> None:
        """Test validation fails for invalid user_learning_languages format."""
        params = BaseDictionaryParams(
            translating_term="сырой",
            user_learning_languages="invalid_format",
        )

        with pytest.raises(ValidationError, match="Invalid user_learning_languages format"):
            await generate_base_dictionary_entry(params, ModelType.CLAUDE_SONNET_4)

    @patch("langtools.ai.functions.LLMClient")
    @patch("langtools.ai.functions.create_base_dictionary_chain")
    async def test_successful_generation(
        self, mock_create_chain: Mock, mock_client_class: Mock
    ) -> None:
        """Test successful base dictionary entry generation."""
        # Setup mocks
        mock_client = Mock()
        mock_client_class.return_value = mock_client

        # Create expected result with proper model structure
        expected_result = AiDictionaryEntry(
            headword="сырой",
            source_language="ru",
            meanings=[
                Meaning(
                    headword="сырой",
                    id="сырой-0",
                    canonical_form="сырой",
                    alternate_spellings=[],
                    definition="Не подвергшийся тепловой обработке",
                    part_of_speech="прилагательное",
                    morphology="качественное прилагательное",
                    register="нейтральный",
                    frequency="common",
                    etymology="от праславянского *syrъ",
                    difficulty_level="intermediate",
                    learning_priority="high",
                    pronunciation="ˈsɨrəj",
                    example_sentences=["Сырое мясо", "Сырые овощи"],
                )
            ],
        )

        mock_client.generate_with_parser_base = AsyncMock(return_value=expected_result)
        mock_chain = Mock()
        mock_create_chain.return_value = mock_chain

        # Test parameters
        params = BaseDictionaryParams(translating_term="сырой", user_learning_languages="en:1,ru:2")

        # Execute function
        result = await generate_base_dictionary_entry(params, ModelType.CLAUDE_SONNET_4)

        # Verify result
        assert result == expected_result
        assert result.source_language == "ru"
        assert len(result.meanings) == 1
        assert result.meanings[0].id == "сырой-0"

        # Verify mocks were called correctly
        mock_client_class.assert_called_once_with(ModelType.CLAUDE_SONNET_4)
        mock_create_chain.assert_called_once_with(model=mock_client.model, params=params)  # type: ignore[misc]
        mock_client.generate_with_parser_base.assert_called_once_with(mock_chain)  # type: ignore[misc]


class TestGenerateMeaningTranslations:
    """Test cases for generate_meaning_translations function."""

    async def test_validate_empty_meanings(self) -> None:
        """Test validation fails for entry with no meanings."""
        base_entry = AiDictionaryEntry(headword="test", source_language="ru", meanings=[])
        params = TranslationParams(entry=base_entry, translation_language="en")

        with pytest.raises(
            ValidationError, match="Dictionary entry must have at least one meaning"
        ):
            await generate_meaning_translations(params, ModelType.CLAUDE_SONNET_4)

    async def test_validate_invalid_translation_language(self) -> None:
        """Test validation fails for invalid translation_language format."""
        base_entry = AiDictionaryEntry(
            headword="test",
            source_language="ru",
            meanings=[
                Meaning(
                    headword="test",
                    id="test-0",
                    canonical_form="test",
                    alternate_spellings=[],
                    definition="test definition",
                    part_of_speech="noun",
                    morphology="noun",
                    register="neutral",
                    frequency="common",
                    etymology="test",
                    difficulty_level="beginner",
                    learning_priority="high",
                    pronunciation="test",
                    example_sentences=["test", "example"],
                )
            ],
        )
        params = TranslationParams(entry=base_entry, translation_language="invalid")

        with pytest.raises(ValidationError, match="Invalid translation_language format"):
            await generate_meaning_translations(params, ModelType.CLAUDE_SONNET_4)


class TestGenerateDictionaryWorkflow:
    """Test cases for generate_dictionary_workflow function."""

    @patch("langtools.ai.functions.generate_meaning_translations")
    @patch("langtools.ai.functions.generate_base_dictionary_entry")
    async def test_successful_workflow(
        self, mock_base_entry: Mock, mock_translations: Mock
    ) -> None:
        """Test successful dictionary workflow execution."""
        # Setup mock results
        base_entry = AiDictionaryEntry(
            headword="сырой",
            source_language="ru",
            meanings=[
                Meaning(
                    headword="сырой",
                    id="сырой-0",
                    canonical_form="сырой",
                    alternate_spellings=[],
                    definition="Не подвергшийся тепловой обработке",
                    part_of_speech="прилагательное",
                    morphology="качественное прилагательное",
                    register="нейтральный",
                    frequency="common",
                    etymology="от праславянского *syrъ",
                    difficulty_level="intermediate",
                    learning_priority="high",
                    pronunciation="ˈsɨrəj",
                    example_sentences=["Сырое мясо", "Сырые овощи"],
                )
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

        mock_base_entry.return_value = base_entry
        mock_translations.return_value = translations

        # Test parameters
        params = DictionaryEntryParams(
            translating_term="сырой",
            user_learning_languages="en:1,ru:2",
            translation_language="en",
        )

        # Execute workflow
        result = await generate_dictionary_workflow(params, ModelType.CLAUDE_SONNET_4)

        # Verify result
        assert isinstance(result, DictionaryWorkflowResult)
        assert result.entry == base_entry
        assert result.translations == translations

        # Verify calls
        mock_base_entry.assert_called_once()
        mock_translations.assert_called_once()


class TestLegacyGenerateDictionaryEntry:
    """Test cases for legacy generate_dictionary_entry function."""

    @patch("langtools.ai.functions.generate_base_dictionary_entry")
    async def test_legacy_function_calls_base_entry(self, mock_base_entry: Mock) -> None:
        """Test that legacy function calls the base entry generator."""
        base_entry = AiDictionaryEntry(headword="test", source_language="en", meanings=[])
        mock_base_entry.return_value = base_entry

        params = DictionaryEntryParams(
            translating_term="test",
            user_learning_languages="en:1",
            translation_language="es",
        )

        result = await generate_dictionary_entry(params, ModelType.CLAUDE_SONNET_4)

        assert result == base_entry
        mock_base_entry.assert_called_once()
