"""
Manual tests for AI functions.
Run with: python -m langtools.ai.test_manual
"""

import asyncio
import logging
import os

from dotenv import load_dotenv

from langtools.ai.debug import configure_debug_logging
from langtools.ai.functions import generate_dictionary_workflow
from langtools.ai.models import DictionaryEntryParams, ModelType

# Load environment variables from .env file
load_dotenv()

# Configure logging to see langtools logs in normal execution
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

# Enable LangChain debug logging (same as debug mode)
os.environ["LANGTOOLS_DEBUG"] = "true"
configure_debug_logging()


async def test_workflow_russian_to_english():
    """Test dictionary workflow with Russian to English translation."""

    # Check if API keys are set
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("⚠️  ANTHROPIC_API_KEY not set. Please set it to test with Claude models.")
        return

    print("🧪 Testing dictionary entry generation for Russian word 'жёсткий'")
    print("=" * 60)

    # Create parameters for Russian word (from design document example)
    params = DictionaryEntryParams(
        translating_term="сырой",
        user_learning_languages="en:1,ru:2",
        translation_language="en",
    )

    try:
        result = await generate_dictionary_workflow(params, ModelType.CLAUDE_SONNET_4)
        print(f"Source Language: {result.entry.source_language}")
        print(f"Headword: {result.entry.headword}")
        print(f"Number of meanings: {len(result.entry.meanings)}")
        print(f"Number of translations: {len(result.translations)}")

        for i, meaning in enumerate(result.entry.meanings):
            print(f"\n--- Meaning {i + 1} ---")
            print(f"   ID: {meaning.id}")
            print(f"   Canonical Form: {meaning.canonical_form}")
            print(f"   Definition: {meaning.definition}")
            print(f"   Part of Speech: {meaning.part_of_speech}")
            print(f"   Pronunciation: {meaning.pronunciation}")
            print(f"   Example Sentences: {meaning.example_sentences}")
            if meaning.synonyms:
                print(f"   Synonyms: {meaning.synonyms}")

        print("\n" + "=" * 50)
        print("TRANSLATIONS:")
        print("=" * 50)

        for i, translation in enumerate(result.translations):
            print(f"\n--- Translation {i + 1} ---")
            print(f"   Meaning ID: {translation.meaning_id}")
            print(f"   Translation: {translation.translation}")
            print(f"   Definition: {translation.definition}")
            print(f"   Pronunciation: {translation.pronunciation}")
            print(f"   Pronunciation Tips: {translation.pronunciation_tips}")
            print(f"   Example Translations: {translation.example_sentences_translations}")

    except Exception as e:
        logger.error(f"Test failed: {e}")
        raise


async def main():
    """Run manual tests."""
    print("🧪 Running manual dictionary workflow tests...")
    print("=" * 80)

    await test_workflow_russian_to_english()

    print("\n✅ All manual tests completed successfully!")


if __name__ == "__main__":
    asyncio.run(main())
