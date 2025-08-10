"""Integration tests for dictionary endpoints."""

from typing import TypedDict, cast

import pytest
from httpx import AsyncClient


class TestUserData(TypedDict):
    """Test user data type."""

    name: str
    email: str
    password: str
    is_e2e_test: bool


async def get_auth_token(client: AsyncClient, test_user_data: TestUserData) -> str:
    """Helper function to register a user and get auth token."""
    # Register user
    await client.post("/auth/register", json=test_user_data)

    # Login to get token
    login_data = {
        "username": test_user_data["email"],
        "password": test_user_data["password"],
    }
    response = await client.post("/auth/login", data=login_data)
    assert response.status_code == 200

    token_response = cast(dict[str, str], response.json())
    return token_response["access_token"]


@pytest.mark.asyncio
async def test_generate_dictionary_entry_basic(
    client: AsyncClient, test_user_data: TestUserData
) -> None:
    """Test basic dictionary entry generation."""
    # Get auth token
    token = await get_auth_token(client, test_user_data)
    headers = {"Authorization": f"Bearer {token}"}

    # Generate dictionary entry
    request_data = {
        "term": "hello",
        "translation_language": "es",
    }

    response = await client.post("/dictionary_entry/generate", json=request_data, headers=headers)
    assert response.status_code == 200

    result = cast(dict[str, object], response.json())
    assert "entry" in result
    assert "translations" in result

    # Verify entry structure
    entry = cast(dict[str, object], result["entry"])
    assert cast(str, entry["headword"]) == "hello"
    assert "source_language" in entry
    assert "meanings" in entry
    meanings = cast(list[dict[str, object]], entry["meanings"])
    assert len(meanings) > 0

    # Verify translations
    translations = cast(list[dict[str, object]], result["translations"])
    assert len(translations) > 0
    for translation in translations:
        assert "meaning_local_id" in translation
        assert "headword" in translation


@pytest.mark.asyncio
async def test_generate_dictionary_entry_cached(
    client: AsyncClient, test_user_data: TestUserData
) -> None:
    """Test that repeated calls use cached data."""
    # Get auth token
    token = await get_auth_token(client, test_user_data)
    headers = {"Authorization": f"Bearer {token}"}

    # Generate dictionary entry first time
    request_data = {
        "term": "test",
        "translation_language": "fr",
    }

    response1 = await client.post("/dictionary_entry/generate", json=request_data, headers=headers)
    assert response1.status_code == 200
    result1 = cast(dict[str, object], response1.json())

    # Generate again with same parameters - should use cache
    response2 = await client.post("/dictionary_entry/generate", json=request_data, headers=headers)
    assert response2.status_code == 200
    result2 = cast(dict[str, object], response2.json())

    # Results should be identical
    result1_entry = cast(dict[str, object], result1["entry"])
    result2_entry = cast(dict[str, object], result2["entry"])
    assert cast(str, result1_entry["headword"]) == cast(str, result2_entry["headword"])
    assert cast(str, result1_entry["source_language"]) == cast(
        str, result2_entry["source_language"]
    )
    assert len(cast(list[dict[str, object]], result1_entry["meanings"])) == len(
        cast(list[dict[str, object]], result2_entry["meanings"])
    )


@pytest.mark.asyncio
async def test_generate_dictionary_entry_regenerate_full(
    client: AsyncClient, test_user_data: TestUserData
) -> None:
    """Test forcing full regeneration."""
    # Get auth token
    token = await get_auth_token(client, test_user_data)
    headers = {"Authorization": f"Bearer {token}"}

    # Generate dictionary entry first time
    request_data = {
        "term": "computer",
        "translation_language": "de",
    }

    response1 = await client.post("/dictionary_entry/generate", json=request_data, headers=headers)
    assert response1.status_code == 200

    # Force regeneration
    request_data["regenerate_full"] = True  # type: ignore[typeddict-item]

    response2 = await client.post("/dictionary_entry/generate", json=request_data, headers=headers)
    assert response2.status_code == 200

    # Both should succeed but may have different results due to regeneration
    result2 = cast(dict[str, object], response2.json())
    assert cast(str, cast(dict[str, object], result2["entry"])["headword"]) == "computer"
    translations2 = cast(list[dict[str, object]], result2["translations"])
    assert len(translations2) > 0


@pytest.mark.asyncio
async def test_generate_dictionary_entry_regenerate_translations_only(
    client: AsyncClient, test_user_data: TestUserData
) -> None:
    """Test regenerating only translations."""
    # Get auth token
    token = await get_auth_token(client, test_user_data)
    headers = {"Authorization": f"Bearer {token}"}

    # Generate dictionary entry first time
    request_data = {
        "term": "book",
        "translation_language": "ja",
    }

    response1 = await client.post("/dictionary_entry/generate", json=request_data, headers=headers)
    assert response1.status_code == 200
    result1 = cast(dict[str, object], response1.json())

    # Regenerate translations only
    request_data["regenerate_translations"] = True  # type: ignore[typeddict-item]

    response2 = await client.post("/dictionary_entry/generate", json=request_data, headers=headers)
    assert response2.status_code == 200
    result2 = cast(dict[str, object], response2.json())

    # Entry should be the same, translations may differ
    result1_entry = cast(dict[str, object], result1["entry"])
    result2_entry = cast(dict[str, object], result2["entry"])
    assert cast(str, result1_entry["headword"]) == cast(str, result2_entry["headword"])
    assert cast(str, result1_entry["source_language"]) == cast(
        str, result2_entry["source_language"]
    )
    translations2 = cast(list[dict[str, object]], result2["translations"])
    assert len(translations2) > 0


@pytest.mark.asyncio
async def test_generate_dictionary_entry_different_languages(
    client: AsyncClient, test_user_data: TestUserData
) -> None:
    """Test generating translations for different languages from same base entry."""
    # Get auth token
    token = await get_auth_token(client, test_user_data)
    headers = {"Authorization": f"Bearer {token}"}

    term = "water"

    # Generate for Spanish
    response_es = await client.post(
        "/dictionary_entry/generate",
        json={"term": term, "translation_language": "es"},
        headers=headers,
    )
    assert response_es.status_code == 200
    result_es = cast(dict[str, object], response_es.json())

    # Generate for French - should reuse base entry
    response_fr = await client.post(
        "/dictionary_entry/generate",
        json={"term": term, "translation_language": "fr"},
        headers=headers,
    )
    assert response_fr.status_code == 200
    result_fr = cast(dict[str, object], response_fr.json())

    # Base entries should be identical
    result_es_entry = cast(dict[str, object], result_es["entry"])
    result_fr_entry = cast(dict[str, object], result_fr["entry"])
    assert cast(str, result_es_entry["headword"]) == cast(str, result_fr_entry["headword"])
    assert cast(str, result_es_entry["source_language"]) == cast(
        str, result_fr_entry["source_language"]
    )

    # But translations should be different
    translations_es = cast(list[dict[str, object]], result_es["translations"])
    translations_fr = cast(list[dict[str, object]], result_fr["translations"])
    assert cast(str, translations_es[0]["canonical_form"]) != cast(
        str, translations_fr[0]["canonical_form"]
    )


@pytest.mark.asyncio
async def test_generate_dictionary_entry_unauthenticated(client: AsyncClient) -> None:
    """Test that unauthenticated requests are rejected."""
    request_data = {
        "term": "test",
        "translation_language": "es",
    }

    response = await client.post("/dictionary_entry/generate", json=request_data)
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_generate_dictionary_entry_invalid_language(
    client: AsyncClient, test_user_data: TestUserData
) -> None:
    """Test with invalid language code."""
    # Get auth token
    token = await get_auth_token(client, test_user_data)
    headers = {"Authorization": f"Bearer {token}"}

    request_data = {
        "term": "test",
        "translation_language": "invalid_language_code",
    }

    response = await client.post("/dictionary_entry/generate", json=request_data, headers=headers)
    # The AI might still try to process this, but it should handle gracefully
    # We just check that the endpoint doesn't crash
    assert response.status_code in [200, 400, 503]


@pytest.mark.asyncio
async def test_unicode_storage_and_caching(
    client: AsyncClient, test_user_data: TestUserData
) -> None:
    """Test that Unicode characters are stored properly and caching works."""
    # Get auth token
    token = await get_auth_token(client, test_user_data)
    headers = {"Authorization": f"Bearer {token}"}

    # Use a term with Unicode characters that could be problematic
    request_data = {
        "term": "котёл",  # Russian word with special character ё
        "translation_language": "en",
    }

    # First request - should call AI and store in database
    response1 = await client.post("/dictionary_entry/generate", json=request_data, headers=headers)

    # Skip if no API keys (expected in CI)
    if response1.status_code in [500, 503]:
        pytest.skip("AI API not available - expected in test environment")

    assert response1.status_code == 200
    result1 = cast(dict[str, object], response1.json())

    # Verify the response contains the Unicode term correctly
    entry1 = cast(dict[str, object], result1["entry"])
    assert cast(str, entry1["headword"]) == "котёл"
    assert entry1["source_language"]  # Should be detected (likely "ru")

    # Second request with same parameters - should use cache
    response2 = await client.post("/dictionary_entry/generate", json=request_data, headers=headers)
    assert response2.status_code == 200
    result2 = cast(dict[str, object], response2.json())

    # Results should be identical (from cache)
    result1_entry = cast(dict[str, object], result1["entry"])
    result2_entry = cast(dict[str, object], result2["entry"])
    assert cast(str, result1_entry["headword"]) == cast(str, result2_entry["headword"])
    assert cast(str, result1_entry["source_language"]) == cast(
        str, result2_entry["source_language"]
    )
    assert len(cast(list[dict[str, object]], result1_entry["meanings"])) == len(
        cast(list[dict[str, object]], result2_entry["meanings"])
    )

    # The meanings should contain properly formatted Unicode
    for meaning in cast(
        list[dict[str, object]], cast(dict[str, object], result2["entry"])["meanings"]
    ):
        assert cast(str, meaning["headword"]) == "котёл"
        assert cast(str, meaning["canonical_form"]) == "котёл"
        # Definition should not contain escaped Unicode sequences
        if "definition" in meaning:
            assert "\\u" not in cast(str, meaning["definition"])


@pytest.mark.asyncio
async def test_regenerate_full_with_unicode(
    client: AsyncClient, test_user_data: TestUserData
) -> None:
    """Test that regenerate_full works correctly with Unicode terms."""
    # Get auth token
    token = await get_auth_token(client, test_user_data)
    headers = {"Authorization": f"Bearer {token}"}

    request_data = {
        "term": "привет",  # Russian greeting
        "translation_language": "en",
    }

    # First request
    response1 = await client.post("/dictionary_entry/generate", json=request_data, headers=headers)

    # Skip if no API keys
    if response1.status_code in [500, 503]:
        pytest.skip("AI API not available - expected in test environment")

    assert response1.status_code == 200

    # Force full regeneration
    request_data["regenerate_full"] = True  # type: ignore[typeddict-item]

    response2 = await client.post("/dictionary_entry/generate", json=request_data, headers=headers)
    assert response2.status_code == 200

    result2 = cast(dict[str, object], response2.json())
    assert cast(str, cast(dict[str, object], result2["entry"])["headword"]) == "привет"
    # Should not contain escaped Unicode
    assert "\\u" not in str(result2)


@pytest.mark.asyncio
async def test_different_languages_same_term(
    client: AsyncClient, test_user_data: TestUserData
) -> None:
    """Test generating different target languages for the same source term."""
    # Get auth token
    token = await get_auth_token(client, test_user_data)
    headers = {"Authorization": f"Bearer {token}"}

    term = "мир"  # Russian word meaning "world" or "peace"

    # Generate English translation
    response_en = await client.post(
        "/dictionary_entry/generate",
        json={"term": term, "translation_language": "en"},
        headers=headers,
    )

    # Skip if no API keys
    if response_en.status_code in [500, 503]:
        pytest.skip("AI API not available - expected in test environment")

    assert response_en.status_code == 200
    result_en = cast(dict[str, object], response_en.json())

    # Generate French translation - should reuse base entry but create new translations
    response_fr = await client.post(
        "/dictionary_entry/generate",
        json={"term": term, "translation_language": "fr"},
        headers=headers,
    )
    assert response_fr.status_code == 200
    result_fr = cast(dict[str, object], response_fr.json())

    # Base entries should be identical (cached)
    result_en_entry = cast(dict[str, object], result_en["entry"])
    result_fr_entry = cast(dict[str, object], result_fr["entry"])
    assert cast(str, result_en_entry["headword"]) == cast(str, result_fr_entry["headword"])
    assert cast(str, result_en_entry["source_language"]) == cast(
        str, result_fr_entry["source_language"]
    )

    # But we should have different translations
    assert len(cast(list[dict[str, object]], result_en["translations"])) > 0
    assert len(cast(list[dict[str, object]], result_fr["translations"])) > 0


@pytest.mark.asyncio
async def test_regenerate_translations_only(
    client: AsyncClient, test_user_data: TestUserData
) -> None:
    """Test that regenerate_translations works correctly."""
    # Get auth token
    token = await get_auth_token(client, test_user_data)
    headers = {"Authorization": f"Bearer {token}"}

    request_data = {
        "term": "дом",  # Russian word for "house"
        "translation_language": "en",
    }

    # First request
    response1 = await client.post("/dictionary_entry/generate", json=request_data, headers=headers)

    # Skip if no API keys
    if response1.status_code in [500, 503]:
        pytest.skip("AI API not available - expected in test environment")

    assert response1.status_code == 200
    result1 = cast(dict[str, object], response1.json())

    # Regenerate translations only
    request_data["regenerate_translations"] = True  # type: ignore[typeddict-item]

    response2 = await client.post("/dictionary_entry/generate", json=request_data, headers=headers)
    assert response2.status_code == 200
    result2 = cast(dict[str, object], response2.json())

    # Base entry should be the same (cached)
    result1_entry = cast(dict[str, object], result1["entry"])
    result2_entry = cast(dict[str, object], result2["entry"])
    assert cast(str, result1_entry["headword"]) == cast(str, result2_entry["headword"])
    assert cast(str, result1_entry["source_language"]) == cast(
        str, result2_entry["source_language"]
    )

    # Should have translations
    assert len(cast(list[dict[str, object]], result2["translations"])) > 0

    # All text should be properly encoded Unicode, not escape sequences
    assert "\\u" not in str(result2)
