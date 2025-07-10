"""
Tests for AI functions.
"""

from unittest.mock import AsyncMock, Mock, patch

import pytest

from langtools.ai.functions import LLMAPIError, ValidationError, generate_dictionary_entry
from langtools.ai.models import AiDictionaryEntry, DictionaryEntryParams, Meaning, ModelType


class TestGenerateDictionaryEntry:
    """Test cases for generate_dictionary_entry function."""

    def test_validate_empty_translating_term(self):
        """Test validation fails for empty translating term."""
        params = DictionaryEntryParams(
            translating_term="", user_learning_languages="en:1,ru:2", translation_language="en"
        )

        with pytest.raises(ValidationError, match="Translating term cannot be empty"):
            pytest.run(generate_dictionary_entry(params, ModelType.CLAUDE_SONNET_4))

    def test_validate_long_translating_term(self):
        """Test validation fails for overly long translating term."""
        params = DictionaryEntryParams(
            translating_term="a" * 101,  # 101 characters
            user_learning_languages="en:1,ru:2",
            translation_language="en",
        )

        with pytest.raises(ValidationError, match="Translating term too long"):
            pytest.run(generate_dictionary_entry(params, ModelType.CLAUDE_SONNET_4))

    def test_validate_invalid_user_learning_languages(self):
        """Test validation fails for invalid user_learning_languages format."""
        params = DictionaryEntryParams(
            translating_term="сырой",
            user_learning_languages="invalid_format",
            translation_language="en",
        )

        with pytest.raises(ValidationError, match="Invalid user_learning_languages format"):
            pytest.run(generate_dictionary_entry(params, ModelType.CLAUDE_SONNET_4))

    def test_validate_invalid_translation_language(self):
        """Test validation fails for invalid translation_language format."""
        params = DictionaryEntryParams(
            translating_term="сырой",
            user_learning_languages="en:1,ru:2",
            translation_language="invalid",
        )

        with pytest.raises(ValidationError, match="Invalid translation_language format"):
            pytest.run(generate_dictionary_entry(params, ModelType.CLAUDE_SONNET_4))

    @patch("langtools.ai.functions.LLMClient")
    @patch("langtools.ai.functions.create_dictionary_entry_chain")
    async def test_successful_generation(self, mock_create_chain, mock_client_class):
        """Test successful dictionary entry generation."""
        # Setup mocks
        mock_client = Mock()
        mock_client_class.return_value = mock_client

        # Create expected result
        expected_result = AiDictionaryEntry(
            source_language="ru",
            meanings=[
                Meaning(
                    id="сырой-0",
                    neutral_form="сырой",
                    definition_original="Не подвергшийся тепловой обработке",
                    definition_translated="Not subjected to heat treatment",
                    translation="raw, uncooked",
                    pronunciation="ˈsɨrəj",
                    synonyms="необработанный, неприготовленный",
                )
            ],
        )

        mock_client.generate_with_parser = AsyncMock(return_value=expected_result)
        mock_chain = Mock()
        mock_create_chain.return_value = mock_chain

        # Test parameters
        params = DictionaryEntryParams(
            translating_term="сырой", user_learning_languages="en:1,ru:2", translation_language="en"
        )

        # Execute function
        result = await generate_dictionary_entry(params, ModelType.CLAUDE_SONNET_4)

        # Verify result
        assert result == expected_result
        assert result.source_language == "ru"
        assert len(result.meanings) == 1
        assert result.meanings[0].id == "сырой-0"

        # Verify mocks were called correctly
        mock_client_class.assert_called_once_with(ModelType.CLAUDE_SONNET_4)
        mock_create_chain.assert_called_once_with(model=mock_client.model, params=params)
        mock_client.generate_with_parser.assert_called_once_with(mock_chain)

    @patch("langtools.ai.functions.LLMClient")
    @patch("langtools.ai.functions.create_dictionary_entry_chain")
    async def test_fix_meaning_ids(self, mock_create_chain, mock_client_class):
        """Test that meaning IDs are fixed if they don't match expected format."""
        # Setup mocks
        mock_client = Mock()
        mock_client_class.return_value = mock_client

        # Create result with incorrect ID
        result_with_wrong_id = AiDictionaryEntry(
            source_language="ru",
            meanings=[
                Meaning(
                    id="wrong-id",  # This should be fixed to "сырой-0"
                    neutral_form="сырой",
                    definition_original="Test definition",
                    definition_translated="Test definition translated",
                    translation="raw",
                    pronunciation="ˈsɨrəj",
                    synonyms="test synonyms",
                )
            ],
        )

        mock_client.generate_with_parser = AsyncMock(return_value=result_with_wrong_id)
        mock_chain = Mock()
        mock_create_chain.return_value = mock_chain

        # Test parameters
        params = DictionaryEntryParams(
            translating_term="сырой", user_learning_languages="en:1,ru:2", translation_language="en"
        )

        # Execute function
        result = await generate_dictionary_entry(params, ModelType.CLAUDE_SONNET_4)

        # Verify ID was fixed
        assert result.meanings[0].id == "сырой-0"

    @patch("langtools.ai.functions.LLMClient")
    @patch("langtools.ai.functions.create_dictionary_entry_chain")
    async def test_empty_meanings_validation(self, mock_create_chain, mock_client_class):
        """Test validation fails when result has no meanings."""
        # Setup mocks
        mock_client = Mock()
        mock_client_class.return_value = mock_client

        # Create result with no meanings
        result_no_meanings = AiDictionaryEntry(source_language="ru", meanings=[])

        mock_client.generate_with_parser = AsyncMock(return_value=result_no_meanings)
        mock_chain = Mock()
        mock_create_chain.return_value = mock_chain

        # Test parameters
        params = DictionaryEntryParams(
            translating_term="сырой", user_learning_languages="en:1,ru:2", translation_language="en"
        )

        # Execute function and expect ValidationError
        with pytest.raises(ValidationError, match="Generated dictionary entry has no meanings"):
            await generate_dictionary_entry(params, ModelType.CLAUDE_SONNET_4)

    @patch("langtools.ai.functions.LLMClient")
    @patch("langtools.ai.functions.create_dictionary_entry_chain")
    async def test_api_error_handling(self, mock_create_chain, mock_client_class):
        """Test API error handling."""
        # Setup mocks
        mock_client = Mock()
        mock_client_class.return_value = mock_client

        # Mock API error
        mock_client.generate_with_parser = AsyncMock(side_effect=Exception("API timeout"))
        mock_chain = Mock()
        mock_create_chain.return_value = mock_chain

        # Test parameters
        params = DictionaryEntryParams(
            translating_term="сырой", user_learning_languages="en:1,ru:2", translation_language="en"
        )

        # Execute function and expect LLMAPIError
        with pytest.raises(LLMAPIError, match="LLM API call failed"):
            await generate_dictionary_entry(params, ModelType.CLAUDE_SONNET_4)

    @patch("langtools.ai.functions.LLMClient")
    @patch("langtools.ai.functions.create_dictionary_entry_chain")
    async def test_generic_error_handling(self, mock_create_chain, mock_client_class):
        """Test generic error handling."""
        # Setup mocks
        mock_client = Mock()
        mock_client_class.return_value = mock_client

        # Mock generic error
        mock_client.generate_with_parser = AsyncMock(side_effect=Exception("Some other error"))
        mock_chain = Mock()
        mock_create_chain.return_value = mock_chain

        # Test parameters
        params = DictionaryEntryParams(
            translating_term="сырой", user_learning_languages="en:1,ru:2", translation_language="en"
        )

        # Execute function and expect LLMAPIError
        with pytest.raises(LLMAPIError, match="Failed to generate dictionary entry"):
            await generate_dictionary_entry(params, ModelType.CLAUDE_SONNET_4)
