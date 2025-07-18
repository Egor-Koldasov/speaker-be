"""
Tests for LLM client functionality.
"""

from unittest.mock import AsyncMock, Mock, patch

import pytest

from langtools.ai.client import LLMClient
from langtools.ai.models import ModelType


class TestLLMClient:
    """Test cases for LLMClient class."""

    @patch("langtools.ai.client.ChatOpenAI")
    def test_create_openai_model(self, mock_chat_openai: Mock) -> None:
        """Test creating OpenAI model."""
        mock_model = Mock()
        mock_chat_openai.return_value = mock_model

        client = LLMClient(ModelType.GPT4)

        assert client.model_type == ModelType.GPT4
        assert client.model == mock_model
        mock_chat_openai.assert_called_once_with(
            model="gpt-4", temperature=0.3, max_tokens=6000, timeout=180
        )

    @patch("langtools.ai.client.ChatOpenAI")
    def test_create_gpt35_model(self, mock_chat_openai: Mock) -> None:
        """Test creating GPT-3.5 model."""
        mock_model = Mock()
        mock_chat_openai.return_value = mock_model

        client = LLMClient(ModelType.GPT3_5)

        assert client.model_type == ModelType.GPT3_5
        assert client.model == mock_model
        mock_chat_openai.assert_called_once_with(
            model="gpt-3.5-turbo", temperature=0.3, max_tokens=4000, timeout=180
        )

    @patch("langtools.ai.client.ChatAnthropic")
    def test_create_claude_model(self, mock_chat_anthropic: Mock) -> None:
        """Test creating Claude model."""
        mock_model = Mock()
        mock_chat_anthropic.return_value = mock_model

        client = LLMClient(ModelType.CLAUDE_SONNET)

        assert client.model_type == ModelType.CLAUDE_SONNET
        assert client.model == mock_model
        mock_chat_anthropic.assert_called_once_with(
            model="claude-3-5-sonnet-20241022", temperature=0.3, max_tokens=8000, timeout=180
        )

    @patch("langtools.ai.client.ChatAnthropic")
    def test_create_claude_sonnet_4_model(self, mock_chat_anthropic: Mock) -> None:
        """Test creating Claude Sonnet 4 model."""
        mock_model = Mock()
        mock_chat_anthropic.return_value = mock_model

        client = LLMClient(ModelType.CLAUDE_SONNET_4)

        assert client.model_type == ModelType.CLAUDE_SONNET_4
        assert client.model == mock_model
        mock_chat_anthropic.assert_called_once_with(
            model="claude-sonnet-4-0", temperature=0.3, max_tokens=8000, timeout=180
        )

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

        client = LLMClient(ModelType.GPT4)

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

        client = LLMClient(ModelType.CLAUDE_SONNET)

        # Execute
        result = await client.generate_with_parser(mock_chain)

        # Verify
        assert result == "test_result"
        mock_chain.ainvoke.assert_called_once_with({})  # type: ignore[misc]
