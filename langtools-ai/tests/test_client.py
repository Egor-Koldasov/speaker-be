"""
Tests for LLM client functionality.
"""

from typing import cast
from unittest.mock import AsyncMock, Mock, patch

from langtools.ai.client import LLMClient
from langtools.ai.models import ModelType


class TestLLMClient:
    """Test cases for LLMClient class."""

    @patch("langtools.ai.client.ChatOpenAI")
    def test_create_openai_model(self, mock_chat_openai: Mock) -> None:
        """Test creating OpenAI model."""
        mock_model = Mock()
        mock_chat_openai.return_value = mock_model

        client = LLMClient(ModelType.GPT5_MINI)

        assert client.model_type == ModelType.GPT5_MINI
        assert client.model == mock_model
        # Only verify model selection; do not check temperature or token limits
        assert mock_chat_openai.call_count == 1
        call_args = cast(tuple[tuple[object, ...], dict[str, object]], mock_chat_openai.call_args)
        kwargs = call_args[1]
        assert kwargs.get("model") == "gpt-5-mini"

    @patch("langtools.ai.client.ChatAnthropic")
    def test_create_claude_sonnet_4_model(self, mock_chat_anthropic: Mock) -> None:
        """Test creating Claude Sonnet 4 model."""
        mock_model = Mock()
        mock_chat_anthropic.return_value = mock_model

        client = LLMClient(ModelType.CLAUDE_SONNET_4)

        assert client.model_type == ModelType.CLAUDE_SONNET_4
        assert client.model == mock_model
        # Only verify model selection; do not check temperature or token limits
        assert mock_chat_anthropic.call_count == 1
        call_args = cast(
            tuple[tuple[object, ...], dict[str, object]], mock_chat_anthropic.call_args
        )
        kwargs = call_args[1]
        assert kwargs.get("model") == "claude-sonnet-4-0"

    @patch("langtools.ai.client.ChatOpenAI")
    @patch("langtools.ai.client.get_openai_callback")
    async def test_generate_with_parser_openai(
        self, mock_callback: Mock, mock_chat_openai: Mock
    ) -> None:
        """Test generate_with_parser with OpenAI model."""
        # Setup mocks
        mock_model = Mock()
        mock_chat_openai.return_value = mock_model

        mock_cb = Mock()
        mock_cb.total_cost = 0.0025
        mock_callback.return_value.__enter__.return_value = mock_cb  # type: ignore[misc]
        mock_callback.return_value.__exit__.return_value = None  # type: ignore[misc]

        mock_chain = Mock()
        mock_chain.ainvoke = AsyncMock(return_value="test_result")

        client = LLMClient(ModelType.GPT5_MINI)

        # Execute
        result = await client.generate_with_parser(mock_chain)

        # Verify
        assert result == "test_result"
        mock_chain.ainvoke.assert_called_once_with({})  # type: ignore[misc]
        mock_callback.assert_called_once()

    @patch("langtools.ai.client.ChatAnthropic")
    async def test_generate_with_parser_claude(self, mock_chat_anthropic: Mock) -> None:
        """Test generate_with_parser with Claude model."""
        # Setup mocks
        mock_model = Mock()
        mock_chat_anthropic.return_value = mock_model

        mock_chain = Mock()
        mock_chain.ainvoke = AsyncMock(return_value="test_result")

        client = LLMClient(ModelType.CLAUDE_HAIKU_3_5)

        # Execute
        result = await client.generate_with_parser(mock_chain)

        # Verify
        assert result == "test_result"
        mock_chain.ainvoke.assert_called_once_with({})  # type: ignore[misc]
