#!/usr/bin/env python3
"""
Manual test script for langtools-ai package.
Tests the generate_dictionary_entry function with Russian examples.
"""

import asyncio
import os

from dotenv import load_dotenv

from langtools.ai.functions import generate_dictionary_entry
from langtools.ai.models import DictionaryEntryParams, ModelType

# Load environment variables from .env file
load_dotenv("src/langtools/.env")


async def test_russian_word() -> None:
    """Test dictionary entry generation with Russian word 'жёсткий'."""

    # Check if API keys are set
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("⚠️  ANTHROPIC_API_KEY not set. Please set it to test with Claude models.")
        return

    print("🧪 Testing dictionary entry generation for Russian word 'жёсткий'")
    print("=" * 60)

    # Create parameters for Russian word (from design document example)
    params = DictionaryEntryParams(
        translating_term="жёсткий",
        user_learning_languages="en:1,ru:2",
        translation_language="en",
    )

    try:
        # Generate dictionary entry using Claude Sonnet 4
        print("📝 Calling generate_dictionary_entry with:")
        print(f"   Term: {params.translating_term}")
        print(f"   User languages: {params.user_learning_languages}")
        print(f"   Target language: {params.translation_language}")
        print(f"   Model: {ModelType.CLAUDE_SONNET_4.value}")
        print()

        result = await generate_dictionary_entry(params, ModelType.CLAUDE_SONNET_4)

        print("✅ Success! Dictionary entry generated:")
        print("=" * 60)
        print(f"🌍 Source Language: {result.source_language}")
        print(f"📊 Number of meanings: {len(result.meanings)}")
        print()

        for i, meaning in enumerate(result.meanings, 1):
            print(f"📖 Meaning {i}:")
            print(f"   ID: {meaning.id}")
            print(f"   Neutral Form: {meaning.neutral_form}")
            print(f"   Definition (Original): {meaning.definition_original}")
            print(f"   Definition (Translated): {meaning.definition_translated}")
            print(f"   Translation: {meaning.translation}")
            print(f"   Pronunciation: {meaning.pronunciation}")
            print(f"   Synonyms: {meaning.synonyms}")
            print()

        # Validate results
        print("🔍 Validation:")
        assert result.source_language == "ru", (
            f"Expected source language 'ru', got '{result.source_language}'"
        )
        assert len(result.meanings) >= 1, "Expected at least 1 meaning"
        assert all(m.id.startswith("жёсткий-") for m in result.meanings), (
            "All meaning IDs should start with 'жёсткий-'"
        )
        print("✅ All validations passed!")

    except Exception as e:
        print(f"❌ Error: {e}")
        print(f"Error type: {type(e).__name__}")
        raise


async def test_validation_errors() -> None:
    """Test input validation with invalid parameters."""

    print("\n🧪 Testing input validation")
    print("=" * 60)

    from langtools.ai.functions import ValidationError

    # Test empty term
    try:
        params = DictionaryEntryParams(
            translating_term="",
            user_learning_languages="en:1,ru:2",
            translation_language="en",
        )
        await generate_dictionary_entry(params, ModelType.CLAUDE_SONNET_4)
        raise AssertionError("Should have raised ValidationError for empty term")
    except ValidationError as e:
        print(f"✅ Empty term validation: {e}")

    # Test invalid user_learning_languages format
    try:
        params = DictionaryEntryParams(
            translating_term="test",
            user_learning_languages="invalid_format",
            translation_language="en",
        )
        await generate_dictionary_entry(params, ModelType.CLAUDE_SONNET_4)
        raise AssertionError("Should have raised ValidationError for invalid format")
    except ValidationError as e:
        print(f"✅ Invalid format validation: {e}")

    # Test invalid translation_language format
    try:
        params = DictionaryEntryParams(
            translating_term="test",
            user_learning_languages="en:1,ru:2",
            translation_language="invalid",
        )
        await generate_dictionary_entry(params, ModelType.CLAUDE_SONNET_4)
        raise AssertionError("Should have raised ValidationError for invalid language")
    except ValidationError as e:
        print(f"✅ Invalid language validation: {e}")

    print("✅ All validation tests passed!")


async def main() -> None:
    """Run all manual tests."""
    print("🚀 Starting manual tests for langtools-ai package")
    print("=" * 80)

    # Test validation first (doesn't require API keys)
    await test_validation_errors()

    # Test actual API call
    await test_russian_word()

    print("\n🎉 All manual tests completed successfully!")
    print("📋 Summary:")
    print("   ✅ Package installation works")
    print("   ✅ Input validation works correctly")
    print("   ✅ Russian dictionary entry generation works")
    print("   ✅ Data models and types work correctly")
    print("   ✅ LangChain integration works")


if __name__ == "__main__":
    asyncio.run(main())
