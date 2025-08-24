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
)
from langtools.ai.models import (
    AiDictionaryEntry,
    AiMeaning,
    BaseDictionaryParams,
    DictionaryEntryParams,
    DictionaryWorkflowResult,
    ModelType,
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
                AiMeaning(
                    headword="сырой",
                    local_id="сырой-1",
                    canonical_form="сырой",
                    definition="Не подвергшийся тепловой обработке",
                    part_of_speech="прилагательное",
                    # alternate_spellings=[],
                    # morphology="качественное прилагательное",
                    # register="нейтральный",
                    # frequency="common",
                    # etymology="от праславянского *syrъ",
                    # difficulty_level="intermediate",
                    # learning_priority="high",
                    # pronunciation="ˈsɨrəj",
                    # example_sentences=["Сырое мясо", "Сырые овощи"],
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
        assert result.meanings[0].local_id == "сырой-1"

        # Verify mocks were called correctly
        mock_client_class.assert_called_once_with(ModelType.CLAUDE_SONNET_4)
        mock_create_chain.assert_called_once_with(model=mock_client.model, params=params)  # type: ignore[misc]
        mock_client.generate_with_parser_base.assert_called_once_with(mock_chain)  # type: ignore[misc]


class TestGenerateDictionaryWorkflow:
    """Test cases for generate_dictionary_workflow function."""

    @patch("langtools.ai.functions.generate_base_dictionary_entry")
    async def test_successful_workflow(self, mock_base_entry: Mock) -> None:
        """Test successful dictionary workflow execution."""
        # Setup mock results
        base_entry = AiDictionaryEntry(
            headword="сырой",
            source_language="ru",
            meanings=[
                AiMeaning(
                    headword="сырой",
                    local_id="сырой-0",
                    canonical_form="сырой",
                    definition="Не подвергшийся тепловой обработке",
                    part_of_speech="прилагательное",
                    # alternate_spellings=[],
                    # morphology="качественное прилагательное",
                    # register="нейтральный",
                    # frequency="common",
                    # etymology="от праславянского *syrъ",
                    # difficulty_level="intermediate",
                    # learning_priority="high",
                    # pronunciation="ˈsɨrəj",
                    # example_sentences=["Сырое мясо", "Сырые овощи"],
                )
            ],
        )

        mock_base_entry.return_value = base_entry

        # Test parameters
        params = DictionaryEntryParams(
            translating_term="сырой",
            user_learning_languages="en:1,ru:2",
        )

        # Execute workflow
        result = await generate_dictionary_workflow(params, ModelType.CLAUDE_SONNET_4)

        # Verify result
        assert isinstance(result, DictionaryWorkflowResult)
        assert result.entry == base_entry

        # Verify calls
        mock_base_entry.assert_called_once()


class TestLegacyGenerateDictionaryEntry:
    """Test cases for legacy generate_dictionary_entry function."""

    @patch("langtools.ai.functions.generate_base_dictionary_entry")
    async def test_legacy_function_calls_base_entry(self, mock_base_entry: Mock) -> None:
        """Test that legacy function calls the base entry generator."""
        base_entry = AiDictionaryEntry(
            headword="test",
            source_language="en",
            meanings=[
                AiMeaning(
                    headword="test",
                    local_id="test-1",
                    canonical_form="test",
                    definition="test",
                    part_of_speech="noun",
                    # alternate_spellings=[],
                    # morphology="noun",
                    # register="neutral",
                    # frequency="common",
                    # etymology="test",
                    # difficulty_level="beginner",
                    # learning_priority="high",
                    # pronunciation="tɛst",
                    # example_sentences=["a test", "another"],
                )
            ],
        )
        mock_base_entry.return_value = base_entry

        params = DictionaryEntryParams(
            translating_term="test",
            user_learning_languages="en:1",
        )

        result = await generate_dictionary_entry(params, ModelType.CLAUDE_SONNET_4)

        assert result == base_entry
        mock_base_entry.assert_called_once()
