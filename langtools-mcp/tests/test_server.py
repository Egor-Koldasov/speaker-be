"""
Tests for MCP server functionality.
"""

from unittest.mock import AsyncMock, MagicMock, patch

from langtools.mcp.server import generate_dictionary_entry


class TestGenerateDictionaryEntryTool:
    """Test cases for generate_dictionary_entry."""

    @patch("langtools.mcp.api.call_api_with_token")
    async def test_successful_generation(self, mock_api_call: AsyncMock) -> None:
        """Test successful dictionary entry generation via MCP tool."""
        # Mock the API response
        api_response = {
            "dictionary_entry": {
                "id": "test-entry-id",
                "headword": "сырой",
                "source_language": "ru",
            },
            "dictionary_entry_translation": {
                "id": "test-translation-id",
                "translation_language": "en",
            },
            "r_user_dictionary_entry": {
                "id": "test-user-entry-id",
            },
        }

        mock_api_call.return_value = api_response
        mock_context = MagicMock()

        # Call the MCP tool
        result = await generate_dictionary_entry(
            context=mock_context,
            translating_term="сырой",
            translation_language="en",
            model="claude-sonnet-4-0",
        )

        # Verify result is the API response
        assert result == api_response

        # Verify API was called correctly
        mock_api_call.assert_called_once_with(
            context=mock_context,
            endpoint="/dictionary_entry/generate",
            method="POST",
            json_data={
                "term": "сырой",
                "translation_language": "en",
                "model": "claude-sonnet-4-0",
                "regenerate_full": False,
                "regenerate_translations": False,
            },
            timeout=300.0,
        )

    @patch("langtools.mcp.api.call_api_with_token")
    async def test_english_generation(self, mock_api_call: AsyncMock) -> None:
        """Test English word dictionary generation."""
        # Mock API response for English word
        api_response = {
            "dictionary_entry": {
                "id": "test-entry-id",
                "headword": "hello",
                "source_language": "en",
            },
            "dictionary_entry_translation": {
                "id": "test-translation-id",
                "translation_language": "ru",
            },
            "r_user_dictionary_entry": {
                "id": "test-user-entry-id",
            },
        }

        mock_api_call.return_value = api_response
        mock_context = MagicMock()

        # Call the MCP tool for English to Russian
        result = await generate_dictionary_entry(
            context=mock_context,
            translating_term="hello",
            translation_language="ru",
            model="claude-3-5-haiku-latest",
        )

        # Verify result
        assert result == api_response

        # Verify API call
        mock_api_call.assert_called_once_with(
            context=mock_context,
            endpoint="/dictionary_entry/generate",
            method="POST",
            json_data={
                "term": "hello",
                "translation_language": "ru",
                "model": "claude-3-5-haiku-latest",
                "regenerate_full": False,
                "regenerate_translations": False,
            },
            timeout=300.0,
        )

    @patch("langtools.mcp.api.call_api_with_token")
    async def test_with_regeneration_flags(self, mock_api_call: AsyncMock) -> None:
        """Test generation with regeneration flags."""
        api_response = {
            "dictionary_entry": {"id": "test-entry-id"},
            "dictionary_entry_translation": {"id": "test-translation-id"},
            "r_user_dictionary_entry": {"id": "test-user-entry-id"},
        }

        mock_api_call.return_value = api_response
        mock_context = MagicMock()

        # Test with regeneration flags
        result = await generate_dictionary_entry(
            context=mock_context,
            translating_term="test",
            translation_language="en",
            regenerate_full=True,
            regenerate_translations=True,
        )

        assert result == api_response

        # Verify flags were passed correctly
        mock_api_call.assert_called_once_with(
            context=mock_context,
            endpoint="/dictionary_entry/generate",
            method="POST",
            json_data={
                "term": "test",
                "translation_language": "en",
                "model": "claude-sonnet-4-0",
                "regenerate_full": True,
                "regenerate_translations": True,
            },
            timeout=300.0,
        )
