"""
Tests for MCP server functionality.
"""

import re
from datetime import datetime
from unittest.mock import AsyncMock, MagicMock, patch

from langtools.mcp.server import DatetimeNowResponse, datetime_now, generate_dictionary_entry


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
                "model": "claude-sonnet-4-0",
                "regenerate_full": False,
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
                "model": "claude-3-5-haiku-latest",
                "regenerate_full": False,
            },
            timeout=300.0,
        )

    @patch("langtools.mcp.api.call_api_with_token")
    async def test_with_regeneration_flags(self, mock_api_call: AsyncMock) -> None:
        """Test generation with regeneration flags."""
        api_response = {
            "dictionary_entry": {"id": "test-entry-id"},
            "r_user_dictionary_entry": {"id": "test-user-entry-id"},
        }

        mock_api_call.return_value = api_response
        mock_context = MagicMock()

        # Test with regeneration flags
        result = await generate_dictionary_entry(
            context=mock_context,
            translating_term="test",
            regenerate_full=True,
        )

        assert result == api_response

        # Verify flags were passed correctly
        mock_api_call.assert_called_once_with(
            context=mock_context,
            endpoint="/dictionary_entry/generate",
            method="POST",
            json_data={
                "term": "test",
                "model": "gpt-5-mini",
                "regenerate_full": True,
            },
            timeout=300.0,
        )


class TestDatetimeNowTool:
    """Test cases for datetime_now."""

    async def test_returns_iso_format_string(self) -> None:
        """Test that datetime_now returns a valid ISO format string with timezone."""
        result = await datetime_now()

        # Should be a string
        assert isinstance(result, DatetimeNowResponse)

        # Should match ISO 8601 format with timezone (YYYY-MM-DDTHH:MM:SS.ssssss+HH:MM)
        iso_pattern = r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{6}[+-]\d{2}:\d{2}$"
        assert re.match(iso_pattern, result.datetime_iso), (
            f"Result '{result}' doesn't match ISO format with timezone"
        )

        # Should be parseable as a datetime
        parsed_datetime = datetime.fromisoformat(result.datetime_iso)
        assert isinstance(parsed_datetime, datetime)

        # Should have timezone information
        assert parsed_datetime.tzinfo is not None, "Datetime should include timezone information"

    async def test_returns_current_datetime(self) -> None:
        """Test that datetime_now returns a datetime close to the current time."""
        before = datetime.now().astimezone()
        result = await datetime_now()
        after = datetime.now().astimezone()

        # Parse the result
        parsed_datetime = datetime.fromisoformat(result.datetime_iso)

        # Should be between before and after timestamps (within a reasonable range)
        assert before <= parsed_datetime <= after, (
            f"Returned datetime {parsed_datetime} not within expected range {before} - {after}"
        )
