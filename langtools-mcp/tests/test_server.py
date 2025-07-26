"""Tests for MCP server functionality."""

from dataclasses import dataclass
from typing import cast
from unittest.mock import AsyncMock, patch

import pytest

from fastmcp.client import Client

from langtools.ai.models import AiDictionaryEntry, Meaning
from langtools.mcp.server import (
    DictionaryEntryRequest,
    create_server,
    generate_dictionary_entry_tool,
)


@pytest.fixture(autouse=True)
def enable_disabled_tool():
    """Enable the disabled generate_dictionary_entry_tool for testing."""
    # Enable the tool before each test
    generate_dictionary_entry_tool.enable()
    yield
    # Disable it again after each test to maintain isolation
    generate_dictionary_entry_tool.disable()


@dataclass
class McpMeaning:
    """Type-safe representation of meaning data."""

    id: str
    neutral_form: str
    definition_original: str
    definition_translated: str
    translation: str
    pronunciation: str
    synonyms: str


@dataclass
class McpToolResponse:
    """Type-safe representation of MCP tool response data."""

    source_language: str
    meanings: list[McpMeaning]


@dataclass
class McpToolSchema:
    """Type-safe representation of MCP tool schema."""

    type: str
    properties: dict[str, object]
    required: list[str]


def convert_to_mcp_response(data: dict[str, object]) -> McpToolResponse:
    """Convert dictionary data to McpToolResponse."""
    meanings_data = cast(list[dict[str, str]], data["meanings"])
    meanings = [
        McpMeaning(
            id=meaning["id"],
            neutral_form=meaning["neutral_form"],
            definition_original=meaning["definition_original"],
            definition_translated=meaning["definition_translated"],
            translation=meaning["translation"],
            pronunciation=meaning["pronunciation"],
            synonyms=meaning["synonyms"],
        )
        for meaning in meanings_data
    ]
    return McpToolResponse(source_language=cast(str, data["source_language"]), meanings=meanings)


class TestMCPServer:
    """Test cases for MCP server functionality."""

    def test_create_server(self) -> None:
        """Test server creation."""
        server = create_server()
        assert server is not None
        assert hasattr(server, "name")
        assert server.name == "LangTools"

    def test_dictionary_entry_request_validation(self) -> None:
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
    async def test_generate_dictionary_entry_tool_via_client(self) -> None:
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

                result_data = cast(dict[str, object] | None, result.data)
                assert result_data is not None
                assert isinstance(result_data, dict)
                # Type-safe conversion to structured response
                data = convert_to_mcp_response(result_data)
                assert data.source_language == "ru"
                assert len(data.meanings) == 1
                meaning = data.meanings[0]
                assert meaning.id == "сырой-0"
                assert meaning.neutral_form == "сырой"
                assert meaning.translation == "raw, uncooked, fresh"

                # Verify the AI function was called
                mock_generate.assert_called_once()


class TestMCPIntegration:
    """Integration tests using fastmcp.Client."""

    @pytest.mark.asyncio
    async def test_mcp_client_server_integration(self) -> None:
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

                result_data = cast(dict[str, object] | None, result.data)
                assert result_data is not None
                assert isinstance(result_data, dict)
                # Type-safe conversion to structured response
                data = convert_to_mcp_response(result_data)
                assert data.source_language == "en"
                assert len(data.meanings) == 1
                meaning = data.meanings[0]
                assert meaning.neutral_form == "hello"
                assert meaning.translation == "привет, здравствуй"

                # Verify AI function was called
                mock_generate.assert_called_once()

    @pytest.mark.asyncio
    async def test_mcp_client_list_tools(self) -> None:
        """Test listing available tools through MCP client."""
        server = create_server()
        client = Client(server)

        async with client:
            tools = await client.list_tools()
            assert len(tools) == 2  # Both tools should be available now
            tool_names = [tool.name for tool in tools]
            assert "generate_dictionary_entry_tool" in tool_names
            assert "check_dictionary_entry" in tool_names

            # Find the generate_dictionary_entry_tool and check its description
            generate_tool = next(
                tool for tool in tools if tool.name == "generate_dictionary_entry_tool"
            )
            tool_description: str | None = generate_tool.description
            assert tool_description is not None
            assert "Generate comprehensive multilingual dictionary entry" in tool_description

    @pytest.mark.asyncio
    async def test_mcp_client_tool_schema(self) -> None:
        """Test tool schema validation through MCP client."""
        server = create_server()
        client = Client(server)

        async with client:
            tools = await client.list_tools()
            # Find the generate_dictionary_entry_tool specifically
            tool = next(tool for tool in tools if tool.name == "generate_dictionary_entry_tool")

            # Check that tool has proper schema
            assert hasattr(tool, "inputSchema")
            schema_data = cast(dict[str, object], tool.inputSchema)
            assert schema_data["type"] == "object"
            assert "properties" in schema_data

            properties = cast(dict[str, object], schema_data["properties"])
            assert "translating_term" in properties
            assert "user_learning_languages" in properties
            assert "translation_language" in properties
            assert "model" in properties

            # Check required fields
            assert "required" in schema_data
            required = cast(list[str], schema_data["required"])
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
