#!/usr/bin/env python3
"""
Real integration test for langtools-mcp server.
This test uses actual API calls and only imports from installed packages.
No mocking - real end-to-end functionality.
"""

import asyncio
import os
import sys
from pathlib import Path
from fastmcp.client import Client

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
    env_vars = {}
    if anthropic_key:
        env_vars["ANTHROPIC_API_KEY"] = anthropic_key
    if openai_key:
        env_vars["OPENAI_API_KEY"] = openai_key
    env_vars["LANGTOOLS_DEBUG"] = "true"

    config = {
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
    available_keys = []
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
            if not result.data:
                print("❌ No data in response")
                return False

            data = result.data
            print(
                f"📖 Generated entry for: "
                f"{data.get('meanings', [{}])[0].get('neutral_form', 'N/A')}"
            )
            print(f"🌍 Source language: {data.get('source_language', 'N/A')}")

            if "meanings" in data and data["meanings"]:
                meaning = data["meanings"][0]
                print(f"🔤 Translation: {meaning.get('translation', 'N/A')}")
                print(f"🗣️ Pronunciation: {meaning.get('pronunciation', 'N/A')}")
                print(
                    f"📚 Definition (original): "
                    f"{meaning.get('definition_original', 'N/A')[:100]}..."
                )
                print(
                    f"📖 Definition (translated): "
                    f"{meaning.get('definition_translated', 'N/A')[:100]}..."
                )
                print(f"🔄 Synonyms: {meaning.get('synonyms', 'N/A')}")

            # Validate required fields
            required_fields = ["source_language", "meanings"]
            missing_fields = [field for field in required_fields if field not in data]
            if missing_fields:
                print(f"❌ Missing required fields: {missing_fields}")
                return False

            if not data["meanings"]:
                print("❌ Empty meanings array")
                return False

            meaning = data["meanings"][0]
            meaning_required = [
                "id",
                "neutral_form",
                "definition_original",
                "definition_translated",
                "translation",
                "pronunciation",
                "synonyms",
            ]
            missing_meaning_fields = [field for field in meaning_required if field not in meaning]
            if missing_meaning_fields:
                print(f"❌ Missing required meaning fields: {missing_meaning_fields}")
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
    models_to_test = []

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

                if result.data and "meanings" in result.data:
                    meaning = result.data["meanings"][0]
                    print(
                        f"✅ {model}: Generated '{meaning.get('neutral_form')}' -> "
                        f"'{meaning.get('translation')}'"
                    )
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
        import langtools.mcp  # noqa: F401
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
