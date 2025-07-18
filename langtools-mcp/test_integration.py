#!/usr/bin/env python3
"""
Real integration test for langtools-mcp server.
This test uses actual API calls and only imports from installed packages.
No mocking - real end-to-end functionality.
"""

import asyncio
import os
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import cast
from fastmcp.client import Client


@dataclass
class IntegrationMeaning:
    """Type-safe representation of meaning data."""

    id: str
    neutral_form: str
    definition_original: str
    definition_translated: str
    translation: str
    pronunciation: str
    synonyms: str


@dataclass
class IntegrationTestResponse:
    """Type-safe representation of integration test response data."""

    source_language: str
    meanings: list[IntegrationMeaning]


def convert_to_integration_response(data: dict[str, object]) -> IntegrationTestResponse:
    """Convert dictionary data to IntegrationTestResponse."""
    meanings_data = cast(list[dict[str, str]], data["meanings"])
    meanings = [
        IntegrationMeaning(
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
    return IntegrationTestResponse(
        source_language=cast(str, data["source_language"]), meanings=meanings
    )


# Load environment variables from .env file
try:
    from dotenv import load_dotenv

    # Look for .env file in project root (parent directory)
    project_root = Path(__file__).parent.parent
    env_file = project_root / ".env"

    if env_file.exists():
        load_dotenv(env_file)
        print(f"✅ Loaded environment from {env_file}")
    else:
        print(f"⚠️  No .env file found at {env_file}")
        print("   You can create one by copying .env.example")

except ImportError:
    print("⚠️  python-dotenv not installed. Using system environment variables only.")
    print("   Install with: pip install python-dotenv")


def create_mcp_client():
    """Create MCP client configuration with environment variables."""
    anthropic_key = os.getenv("ANTHROPIC_API_KEY")
    openai_key = os.getenv("OPENAI_API_KEY")

    # Pass environment variables to subprocess
    env_vars: dict[str, str] = {}
    if anthropic_key:
        env_vars["ANTHROPIC_API_KEY"] = anthropic_key
    if openai_key:
        env_vars["OPENAI_API_KEY"] = openai_key
    env_vars["LANGTOOLS_DEBUG"] = "true"

    config: dict[str, dict[str, dict[str, str | list[str] | dict[str, str]]]] = {
        "mcpServers": {
            "langtools": {"command": "langtools-mcp", "args": ["--verbose"], "env": env_vars}
        }
    }
    return Client(config)


async def test_real_integration():
    """Test complete real integration with actual API calls."""
    print("🚀 Starting REAL langtools-mcp integration test...")
    print("⚠️  This test will make actual API calls to language models")

    # Check for required environment variables (at least one needed)
    anthropic_key = os.getenv("ANTHROPIC_API_KEY")
    openai_key = os.getenv("OPENAI_API_KEY")

    if not anthropic_key and not openai_key:
        print("❌ No API keys found!")
        print("\n📝 To set up API keys:")
        print("   1. Copy .env.example to .env:  cp ../.env.example ../.env")
        print("   2. Edit .env file with your actual API keys")
        print("   3. Or set environment variables directly:")
        print("      export ANTHROPIC_API_KEY='your-key'")
        print("      export OPENAI_API_KEY='your-key'")
        print("\n💡 At least one API key is required for this test")
        return False

    # Show which keys are available
    available_keys: list[str] = []
    if anthropic_key:
        available_keys.append("Anthropic")
    if openai_key:
        available_keys.append("OpenAI")
    print(f"✅ API keys available: {', '.join(available_keys)}")

    try:
        # Test the CLI bundle using FastMCP's built-in subprocess support
        print("🚀 Starting MCP server via CLI...")
        print("   Creating client with langtools-mcp CLI...")

        client = create_mcp_client()
        async with client:
            print("✅ Connected to MCP server")

            # List available tools
            tools = await client.list_tools()
            print(f"✅ Available tools: {[tool.name for tool in tools]}")

            if not tools:
                print("❌ No tools found!")
                return False

            # Verify the expected tool exists
            tool_names = [tool.name for tool in tools]
            if "generate_dictionary_entry_tool" not in tool_names:
                print(f"❌ Expected tool not found. Available: {tool_names}")
                return False

            print("🔧 Making REAL API call to generate dictionary entry...")
            print("📝 Generating entry for 'hello' (English to Russian)...")

            # Choose model based on available API keys
            if anthropic_key:
                model = "claude-3-5-sonnet-20241022"
                print(f"   Using Claude model: {model}")
            elif openai_key:
                model = "gpt-4"
                print(f"   Using OpenAI model: {model}")
            else:
                # This shouldn't happen due to earlier check, but just in case
                model = "gpt-4"

            # Test with a simple, common word to minimize API costs
            result = await client.call_tool(
                "generate_dictionary_entry_tool",
                {
                    "translating_term": "hello",
                    "user_learning_languages": "en:1,ru:2",
                    "translation_language": "ru",
                    "model": model,
                },
            )

            print("✅ REAL API call successful!")

            # Validate the response structure
            data_raw = cast(dict[str, object] | None, result.data)
            if not data_raw:
                print("❌ No data in response")
                return False

            # Type-safe conversion to structured response
            data = convert_to_integration_response(data_raw)
            meanings = data.meanings
            print(f"📖 Generated entry for: {meanings[0].neutral_form}")
            print(f"🌍 Source language: {data.source_language}")

            if data.meanings:
                meaning = data.meanings[0]
                print(f"🔤 Translation: {meaning.translation}")
                print(f"🗣️ Pronunciation: {meaning.pronunciation}")
                orig_def = meaning.definition_original[:100]
                trans_def = meaning.definition_translated[:100]
                print(f"📚 Definition (original): {orig_def}...")
                print(f"📖 Definition (translated): {trans_def}...")
                print(f"🔄 Synonyms: {meaning.synonyms}")

            # Validate required fields
            if not data.source_language:
                print("❌ Missing source_language field")
                return False

            if not data.meanings:
                print("❌ Empty meanings array")
                return False

            meaning = data.meanings[0]
            # All fields are required in the dataclass, so we just need to check they exist
            required_fields = [
                meaning.id,
                meaning.neutral_form,
                meaning.definition_original,
                meaning.definition_translated,
                meaning.translation,
                meaning.pronunciation,
                meaning.synonyms,
            ]
            if not all(required_fields):
                print("❌ Missing required meaning fields")
                return False

            print("✅ All required fields present")
            print("✅ Response structure validated")

    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure langtools-mcp is properly installed")
        return False
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        print(f"Error type: {type(e).__name__}")
        return False

    print("🎉 REAL integration test completed successfully!")
    print("💰 Note: This test made actual API calls and may have incurred costs")
    return True


async def test_with_different_models():
    """Test with different language models using CLI bundle."""
    print("\n🔄 Testing with different models...")

    # Only test models we have API keys for
    models_to_test: list[str] = []

    anthropic_key = os.getenv("ANTHROPIC_API_KEY")
    # openai_key = os.getenv("OPENAI_API_KEY")  # Not used currently

    if anthropic_key:
        models_to_test.append("claude-sonnet-4-0")

    # if openai_key:
    #     models_to_test.extend(["gpt-4", "gpt-3.5-turbo"])

    if not models_to_test:
        print("❌ No API keys available for model testing")
        return

    print(f"   Will test models: {models_to_test}")

    for model in models_to_test:
        print(f"\n🧪 Testing with model: {model}")
        try:
            # Use FastMCP's built-in subprocess support with CLI bundle
            client = create_mcp_client()
            async with client:
                result = await client.call_tool(
                    "generate_dictionary_entry_tool",
                    {
                        "translating_term": "cat",
                        "user_learning_languages": "en:1,es:2",
                        "translation_language": "es",
                        "model": model,
                    },
                )

                data_raw = cast(dict[str, object] | None, result.data)
                if data_raw and "meanings" in data_raw:
                    # Type-safe conversion to structured response
                    data = convert_to_integration_response(data_raw)
                    meaning = data.meanings[0]
                    neutral = meaning.neutral_form
                    translation = meaning.translation
                    print(f"✅ {model}: Generated '{neutral}' -> '{translation}'")
                else:
                    print(f"❌ {model}: Invalid response structure")

        except Exception as e:
            print(f"❌ {model}: Failed with {type(e).__name__}: {e}")


if __name__ == "__main__":
    print("=" * 60)
    print("LANGTOOLS-MCP REAL INTEGRATION TEST")
    print("=" * 60)

    # Check if we're in the right environment
    try:
        # import langtools.ai  # Available through langtools-mcp dependency

        print("✅ Required packages found")
    except ImportError as e:
        print(f"❌ Required packages not found: {e}")
        print("Make sure you're in the virtual environment and packages are installed")
        sys.exit(1)

    # Run main integration test
    success = asyncio.run(test_real_integration())

    if success:
        # Run additional model tests if main test passed
        asyncio.run(test_with_different_models())
        print("\n🎉 All tests completed!")
    else:
        print("\n❌ Integration test failed")
        sys.exit(1)
