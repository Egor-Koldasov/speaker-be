"""
Integration tests for MCP server with real API calls.
NOTE: This test requires a running langtools-main API server with authentication.
It is not intended for automated testing.
Run with: python -m langtools.mcp.test_integration
"""

import asyncio
import logging


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def test_mcp_tool_integration():
    """Test MCP tool with API integration."""
    print("🧪 Testing MCP tool integration with API...")
    print("=" * 80)

    try:
        print("⚠️ Integration test requires API server setup and authentication")
        print("📝 This test is a placeholder for manual integration testing")
        print("🔧 To implement: Set up MCP context with proper authentication token")
        print("🌐 Then call the API-based MCP tools with real endpoints")

        print("🎯 Available MCP tools to test:")
        print("   • generate_dictionary_entry")
        print("   • get_fsrs_records")
        print("   • create_fsrs_record")
        print("   • process_fsrs_review")
        print("   • me (user info)")

        print("🎉 Integration test framework ready (but skipped)!")

    except Exception as e:
        print(f"❌ Test failed with error: {type(e).__name__}: {e}")
        import traceback

        traceback.print_exc()


async def main():
    """Run integration tests."""
    await test_mcp_tool_integration()


if __name__ == "__main__":
    asyncio.run(main())
