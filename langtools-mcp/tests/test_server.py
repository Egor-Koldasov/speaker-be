"""Tests for MCP server functionality."""

from unittest.mock import AsyncMock, patch

import pytest

from fastmcp.client import Client

from langtools.ai.models import AiDictionaryEntry, Meaning
from langtools.mcp.server import DictionaryEntryRequest, create_server


class TestMCPServer:
    """Test cases for MCP server functionality."""

    def test_create_server(self):
        """Test server creation."""
        server = create_server()
        assert server is not None
        assert server.name == "langtools-mcp"

    def test_dictionary_entry_request_validation(self):
        """Test DictionaryEntryRequest validation."""
        # Valid request
        valid_request = DictionaryEntryRequest(
            translating_term="сырой",
            user_learning_languages="en:1,ru:2",
            translation_language="en",
        )
        assert valid_request.translating_term == "сырой"
        assert valid_request.user_learning_languages == "en:1,ru:2"
        assert valid_request.translation_language == "en"
        assert valid_request.model == "claude-3-5-sonnet-20241022"  # default

        # Custom model
        custom_model_request = DictionaryEntryRequest(
            translating_term="test",
            user_learning_languages="en:1",
            translation_language="ru",
            model="gpt-4",
        )
        assert custom_model_request.model == "gpt-4"

    @pytest.mark.asyncio
    async def test_generate_dictionary_entry_tool_via_client(self):
        """Test dictionary entry generation through MCP client."""
        server = create_server()

        # Mock the AI function
        mock_meaning = Meaning(
            id="сырой-0",
            neutral_form="сырой",
            definition_original="Не подвергшийся тепловой обработке",
            definition_translated="Not subjected to heat treatment",
            translation="raw, uncooked, fresh",
            pronunciation="ˈsɨrəj",
            synonyms="необработанный, неприготовленный, свежий",
        )

        mock_result = AiDictionaryEntry(source_language="ru", meanings=[mock_meaning])

        with patch(
            "langtools.mcp.server.generate_dictionary_entry", new_callable=AsyncMock
        ) as mock_generate:
            mock_generate.return_value = mock_result

            client = Client(server)
            async with client:
                result = await client.call_tool(
                    "generate_dictionary_entry_tool",
                    {
                        "translating_term": "сырой",
                        "user_learning_languages": "en:1,ru:2",
                        "translation_language": "en",
                    },
                )

                assert result.data is not None
                assert isinstance(result.data, dict)
                assert result.data["source_language"] == "ru"
                assert len(result.data["meanings"]) == 1
                assert result.data["meanings"][0]["id"] == "сырой-0"
                assert result.data["meanings"][0]["neutral_form"] == "сырой"
                assert result.data["meanings"][0]["translation"] == "raw, uncooked, fresh"

                # Verify the AI function was called
                mock_generate.assert_called_once()


class TestMCPIntegration:
    """Integration tests using fastmcp.Client."""

    @pytest.mark.asyncio
    async def test_mcp_client_server_integration(self):
        """Test MCP client-server integration."""
        server = create_server()

        # Mock the AI function for integration test
        mock_meaning = Meaning(
            id="hello-0",
            neutral_form="hello",
            definition_original="A greeting",
            definition_translated="Приветствие",
            translation="привет, здравствуй",
            pronunciation="həˈləʊ",
            synonyms="hi, greetings",
        )

        mock_result = AiDictionaryEntry(source_language="en", meanings=[mock_meaning])

        with patch(
            "langtools.mcp.server.generate_dictionary_entry", new_callable=AsyncMock
        ) as mock_generate:
            mock_generate.return_value = mock_result

            # Create MCP client and connect
            client = Client(server)
            async with client:
                # Test tool calling
                result = await client.call_tool(
                    "generate_dictionary_entry_tool",
                    {
                        "translating_term": "hello",
                        "user_learning_languages": "ru:1,en:2",
                        "translation_language": "ru",
                    },
                )

                assert result.data is not None
                assert isinstance(result.data, dict)
                assert result.data["source_language"] == "en"
                assert len(result.data["meanings"]) == 1
                assert result.data["meanings"][0]["neutral_form"] == "hello"
                assert result.data["meanings"][0]["translation"] == "привет, здравствуй"

                # Verify AI function was called
                mock_generate.assert_called_once()

    @pytest.mark.asyncio
    async def test_mcp_client_list_tools(self):
        """Test listing available tools through MCP client."""
        server = create_server()
        client = Client(server)

        async with client:
            tools = await client.list_tools()
            assert len(tools) == 1
            assert tools[0].name == "generate_dictionary_entry_tool"
            assert "Generate comprehensive dictionary entry" in tools[0].description

    @pytest.mark.asyncio
    async def test_mcp_client_tool_schema(self):
        """Test tool schema validation through MCP client."""
        server = create_server()
        client = Client(server)

        async with client:
            tools = await client.list_tools()
            tool = tools[0]

            # Check that tool has proper schema
            assert hasattr(tool, "inputSchema")
            schema = tool.inputSchema
            assert schema["type"] == "object"
            assert "properties" in schema

            properties = schema["properties"]
            assert "translating_term" in properties
            assert "user_learning_languages" in properties
            assert "translation_language" in properties
            assert "model" in properties

            # Check required fields
            assert "required" in schema
            required = schema["required"]
            assert "translating_term" in required
            assert "user_learning_languages" in required
            assert "translation_language" in required
            # model should not be required (has default)
            assert "model" not in required

    @pytest.mark.asyncio
    async def test_mcp_client_error_handling(self):
        """Test error handling through MCP client."""
        server = create_server()
        client = Client(server)

        with patch(
            "langtools.mcp.server.generate_dictionary_entry", new_callable=AsyncMock
        ) as mock_generate:
            mock_generate.side_effect = Exception("AI service unavailable")

            async with client:
                with pytest.raises(Exception) as exc_info:
                    await client.call_tool(
                        "generate_dictionary_entry_tool",
                        {
                            "translating_term": "test",
                            "user_learning_languages": "en:1",
                            "translation_language": "ru",
                        },
                    )

                assert "Dictionary entry generation failed" in str(exc_info.value)
                assert "AI service unavailable" in str(exc_info.value)
