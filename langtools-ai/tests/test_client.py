"""
Tests for LLM client functionality.
"""

import pytest
from unittest.mock import Mock, AsyncMock, patch
from langtools.ai.client import LLMClient
from langtools.ai.models import ModelType


class TestLLMClient:
    """Test cases for LLMClient class."""
    
    @patch('langtools.ai.client.ChatOpenAI')
    def test_create_openai_model(self, mock_chat_openai):
        """Test creating OpenAI model."""
        mock_model = Mock()
        mock_chat_openai.return_value = mock_model
        
        client = LLMClient(ModelType.GPT4)
        
        assert client.model_type == ModelType.GPT4
        assert client.model == mock_model
        mock_chat_openai.assert_called_once_with(
            model="gpt-4",
            temperature=0.3,
            max_tokens=800,
            timeout=30
        )
    
    @patch('langtools.ai.client.ChatOpenAI')
    def test_create_gpt35_model(self, mock_chat_openai):
        """Test creating GPT-3.5 model."""
        mock_model = Mock()
        mock_chat_openai.return_value = mock_model
        
        client = LLMClient(ModelType.GPT3_5)
        
        assert client.model_type == ModelType.GPT3_5
        assert client.model == mock_model
        mock_chat_openai.assert_called_once_with(
            model="gpt-3.5-turbo",
            temperature=0.3,
            max_tokens=800,
            timeout=30
        )
    
    @patch('langtools.ai.client.ChatAnthropic')
    def test_create_claude_model(self, mock_chat_anthropic):
        """Test creating Claude model."""
        mock_model = Mock()
        mock_chat_anthropic.return_value = mock_model
        
        client = LLMClient(ModelType.CLAUDE_SONNET)
        
        assert client.model_type == ModelType.CLAUDE_SONNET
        assert client.model == mock_model
        mock_chat_anthropic.assert_called_once_with(
            model="claude-3-5-sonnet-20241022",
            temperature=0.3,
            max_tokens=800,
            timeout=30
        )
    
    @patch('langtools.ai.client.ChatAnthropic')
    def test_create_claude_sonnet_4_model(self, mock_chat_anthropic):
        """Test creating Claude Sonnet 4 model."""
        mock_model = Mock()
        mock_chat_anthropic.return_value = mock_model
        
        client = LLMClient(ModelType.CLAUDE_SONNET_4)
        
        assert client.model_type == ModelType.CLAUDE_SONNET_4
        assert client.model == mock_model
        mock_chat_anthropic.assert_called_once_with(
            model="claude-sonnet-4-0",
            temperature=0.3,
            max_tokens=800,
            timeout=30
        )
    
    def test_unsupported_model_type(self):
        """Test that unsupported model type raises ValueError."""
        # Create a fake model type that's not supported
        with pytest.raises(ValueError, match="Unsupported model type"):
            # This will fail because we can't create an invalid enum value
            # Instead, we'll patch the _create_model method to test this path
            client = LLMClient(ModelType.GPT4)
            client._create_model("invalid_model")
    
    @patch('langtools.ai.client.ChatOpenAI')
    @patch('langtools.ai.client.get_openai_callback')
    async def test_generate_with_parser_openai(self, mock_callback, mock_chat_openai):
        """Test generate_with_parser with OpenAI model."""
        # Setup mocks
        mock_model = Mock()
        mock_chat_openai.return_value = mock_model
        
        mock_cb = Mock()
        mock_cb.total_cost = 0.0025
        mock_callback.return_value.__enter__.return_value = mock_cb
        mock_callback.return_value.__exit__.return_value = None
        
        mock_chain = Mock()
        mock_chain.ainvoke = AsyncMock(return_value="test_result")
        
        client = LLMClient(ModelType.GPT4)
        
        # Execute
        result = await client.generate_with_parser(mock_chain)
        
        # Verify
        assert result == "test_result"
        mock_chain.ainvoke.assert_called_once_with({})
        mock_callback.assert_called_once()
    
    @patch('langtools.ai.client.ChatAnthropic')
    async def test_generate_with_parser_claude(self, mock_chat_anthropic):
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
        mock_chain.ainvoke.assert_called_once_with({})
    
    @patch('langtools.ai.client.ChatOpenAI')
    @patch('langtools.ai.client.get_openai_callback')
    async def test_generate_with_parser_openai_cost_logging(self, mock_callback, mock_chat_openai):
        """Test that OpenAI cost logging works correctly."""
        # Setup mocks
        mock_model = Mock()
        mock_chat_openai.return_value = mock_model
        
        mock_cb = Mock()
        mock_cb.total_cost = 0.0123
        mock_callback.return_value.__enter__.return_value = mock_cb
        mock_callback.return_value.__exit__.return_value = None
        
        mock_chain = Mock()
        mock_chain.ainvoke = AsyncMock(return_value="test_result")
        
        client = LLMClient(ModelType.GPT4)
        
        # Capture printed output
        with patch('builtins.print') as mock_print:
            result = await client.generate_with_parser(mock_chain)
            
            # Verify cost was logged
            mock_print.assert_called_once_with("LLM API cost: $0.0123")
        
        assert result == "test_result"