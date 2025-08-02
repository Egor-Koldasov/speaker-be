"""
Integration tests for MCP server with real LLM calls.
Run with: python -m langtools.mcp.test_integration
"""

import asyncio
import json
import logging
import os
from typing import Dict, Any

from langtools.ai.models import (
    AiDictionaryEntry, 
    DictionaryEntryParams,
    DictionaryWorkflowResult,
    Meaning,
    MeaningTranslation,
    ModelType,
)
from langtools.mcp.server import generate_dictionary_entry_tool


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_mock_meaning(**kwargs) -> Dict[str, Any]:
    """Create a mock meaning dict for testing."""
    return {
        "headword": kwargs.get("headword", ""),
        "id": kwargs.get("id", ""),
        "canonical_form": kwargs.get("canonical_form", ""),
        "alternate_spellings": kwargs.get("alternate_spellings", []),
        "definition": kwargs.get("definition", ""),
        "part_of_speech": kwargs.get("part_of_speech", ""),
        "morphology": kwargs.get("morphology", ""),
        "register": kwargs.get("register", ""),
        "frequency": kwargs.get("frequency", ""),
        "etymology": kwargs.get("etymology", ""),
        "difficulty_level": kwargs.get("difficulty_level", ""),
        "learning_priority": kwargs.get("learning_priority", ""),
        "pronunciation": kwargs.get("pronunciation", ""),
        "example_sentences": kwargs.get("example_sentences", []),
        "synonyms": kwargs.get("synonyms", []),
        "antonyms": kwargs.get("antonyms", []),
    }


class MockMeaning:
    """Mock meaning object for tests."""

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


def create_meaning_obj_from_dict(meaning_dict: dict) -> MockMeaning:
    """Helper to create MockMeaning from dict."""
    return MockMeaning(
        headword=meaning_dict.get("headword", ""),
        id=meaning_dict.get("id", ""),
        canonical_form=meaning_dict.get("canonical_form", ""),
        alternate_spellings=meaning_dict.get("alternate_spellings", []),
        definition=meaning_dict.get("definition", ""),
        part_of_speech=meaning_dict.get("part_of_speech", ""),
        morphology=meaning_dict.get("morphology", ""),
        register=meaning_dict.get("register", ""),
        frequency=meaning_dict.get("frequency", ""),
        etymology=meaning_dict.get("etymology", ""),
        difficulty_level=meaning_dict.get("difficulty_level", ""),
        learning_priority=meaning_dict.get("learning_priority", ""),
        pronunciation=meaning_dict.get("pronunciation", ""),
        example_sentences=meaning_dict.get("example_sentences", []),
        synonyms=meaning_dict.get("synonyms", []),
        antonyms=meaning_dict.get("antonyms", []),
    )


async def test_mcp_tool_integration():
    """Test MCP tool with workflow integration."""
    print("🧪 Testing MCP tool integration with new workflow...")
    print("=" * 80)

    try:
        # Test Russian to English
        print("📝 Testing Russian to English dictionary generation...")
        result = await generate_dictionary_entry_tool(
            translating_term="сырой",
            user_learning_languages="en:1,ru:2",
            translation_language="en",
            model="claude-sonnet-4-0",
        )

        print(f"✅ MCP tool returned result type: {type(result)}")
        
        if isinstance(result, dict):
            print(f"📊 Result keys: {list(result.keys())}")
            
            if "entry" in result:
                entry = result["entry"]
                print(f"🔍 Entry headword: {entry.get('headword', 'N/A')}")
                print(f"🌍 Source language: {entry.get('source_language', 'N/A')}")
                
                meanings = entry.get("meanings", [])
                print(f"📚 Number of meanings: {len(meanings)}")
                
                if meanings:
                    meaning = meanings[0]
                    print(f"📖 First meaning canonical form: {meaning.get('canonical_form', 'N/A')}")
                    print(f"📝 First meaning definition: {meaning.get('definition', 'N/A')[:100]}...")

            if "translations" in result:
                translations = result["translations"]
                print(f"🌐 Number of translations: {len(translations)}")
                
                if translations:
                    translation = translations[0]
                    print(f"🔤 First translation: {translation.get('translation', 'N/A')}")
                    print(f"🗣️ First translation pronunciation: {translation.get('pronunciation', 'N/A')}")

        # Test English to Spanish
        print("\n" + "=" * 50)
        print("📝 Testing English to Spanish dictionary generation...")
        
        result2 = await generate_dictionary_entry_tool(
            translating_term="beautiful",
            user_learning_languages="en:1,es:2",
            translation_language="es",
            model="claude-sonnet-4-0",
        )

        if isinstance(result2, dict) and "entry" in result2:
            entry = result2["entry"]
            print(f"✅ English test - headword: {entry.get('headword', 'N/A')}")
            print(f"🌍 Source language: {entry.get('source_language', 'N/A')}")
            
            if "translations" in result2:
                translations = result2["translations"]
                if translations:
                    print(f"🇪🇸 Spanish translation: {translations[0].get('translation', 'N/A')}")

        print("\n✅ All MCP integration tests completed successfully!")
        return True

    except Exception as e:
        print(f"❌ Integration test failed: {e}")
        logger.exception("Integration test error details:")
        return False


async def test_mock_workflow_result():
    """Test creating mock workflow results for development."""
    print("\n🔧 Testing mock workflow result creation...")
    
    # Create mock base entry
    base_entry_dict = {
        "headword": "test",
        "source_language": "en",
        "meanings": [
            create_mock_meaning(
                headword="test",
                id="test-0",
                canonical_form="test",
                definition="A procedure intended to establish the quality or reliability of something",
                part_of_speech="noun",
                morphology="countable noun",
                register="neutral",
                frequency="common",
                etymology="from Old French test",
                difficulty_level="intermediate",
                learning_priority="medium",
                pronunciation="test",
                example_sentences=["This is a test", "The test was difficult"],
            )
        ]
    }

    # Create mock translations
    translations_dict = [
        {
            "meaning_id": "test-0",
            "headword": "prueba",
            "canonical_form": "prueba",
            "translation_language": "es",
            "translation": "prueba, examen",
            "definition": "Procedimiento para establecer la calidad de algo",
            "part_of_speech": "sustantivo",
            "morphology": "sustantivo femenino",
            "register": "neutral",
            "frequency": "común",
            "etymology": "del latín proba",
            "difficulty_level": "intermedio",
            "learning_priority": "medio",
            "pronunciation": "ˈpɾweβa",
            "pronunciation_tips": "Stressed on first syllable",
            "example_sentences_translations": ["Esta es una prueba", "La prueba fue difícil"],
        }
    ]

    # Convert to objects for inspection
    meanings = [create_meaning_obj_from_dict(m) for m in base_entry_dict["meanings"]]
    if meanings:
        print(f"📚 Mock meaning canonical form: {meanings[0].canonical_form}")
        print(f"📖 Mock meaning definition: {meanings[0].definition}")

    print("✅ Mock workflow result creation successful!")


async def main():
    """Run integration tests."""
    # Check for required environment variables
    required_env_vars = ["ANTHROPIC_API_KEY", "OPENAI_API_KEY"]
    missing_vars = [var for var in required_env_vars if not os.getenv(var)]
    
    if missing_vars:
        print(f"⚠️ Warning: Missing environment variables: {missing_vars}")
        print("Some tests may fail without proper API keys.")
        print("Set ANTHROPIC_API_KEY and/or OPENAI_API_KEY environment variables.")
        print()

    print("🚀 Starting MCP integration tests...")
    print("=" * 80)

    # Run mock tests first
    await test_mock_workflow_result()

    # Run integration tests if API keys are available
    if not missing_vars:
        success = await test_mcp_tool_integration()
        if success:
            print("\n🎉 All integration tests passed!")
        else:
            print("\n❌ Some integration tests failed!")
            exit(1)
    else:
        print("\n⏭️ Skipping real API integration tests due to missing API keys.")
        print("✅ Mock tests completed successfully!")


if __name__ == "__main__":
    asyncio.run(main())