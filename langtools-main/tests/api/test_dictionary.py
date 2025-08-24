"""Integration tests for dictionary endpoints."""

from typing import TypedDict, cast

import pytest
from httpx import AsyncClient

from langtools.ai.models import AiDictionaryEntry, AiMeaning

# DB seeding helpers to avoid AI calls in tests (cache-only mode for e2e users)
from langtools.main.api.database import get_session
from langtools.main.api.pg_queries import dictionary as dictionary_queries
from langtools.main.api.pg_queries.auth_user import find_auth_user_by_email


class TestUserData(TypedDict):
    """Test user data type."""

    name: str
    email: str
    password: str
    is_e2e_test: bool


def _make_ai_entry(term: str, source_language: str = "en") -> AiDictionaryEntry:
    """Create a minimal valid AiDictionaryEntry with one meaning."""
    meaning = AiMeaning(
        headword=term,
        local_id=f"{term}-1",
        canonical_form=term,
        definition=f"Definition of {term}",
        part_of_speech="noun",
        # alternate_spellings=[],
        # semantic_field=None,
        # pronunciation="/term/",
        # tone_notation=None,
        # syllable_count=None,
        # phonetic_variations=None,
        # morphology="N/A",
        # register="neutral",
        # frequency="common",
        # etymology="N/A",
        # difficulty_level="beginner",
        # learning_priority="essential",
        # common_mistakes=None,
        # mnemonic_hints=None,
        # practice_suggestions=None,
        # example_sentences=[f"{term} example 1.", f"{term} example 2."],
        # collocations=None,
        # synonyms=None,
        # antonyms=None,
    )
    return AiDictionaryEntry(headword=term, source_language=source_language, meanings=[meaning])


def _seed_entry_and_optional_translation(user_email: str, term: str) -> None:
    """Seed base entry and optionally a translation for the specified user."""
    auth_user = find_auth_user_by_email(user_email)
    assert auth_user is not None

    with get_session() as session:
        # Reuse existing entry for this term if present to attach multiple translations
        existing_entry = dictionary_queries.find_latest_dictionary_entry_for_user(
            session, auth_user.id, term
        )
        if existing_entry:
            # Use the stored AI entry for translation generation consistency
            ai_entry = existing_entry.get_ai_dictionary_entry()
        else:
            ai_entry = _make_ai_entry(term)
            dictionary_queries.create_dictionary_entry(session, auth_user.id, ai_entry)
        session.commit()


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

    # Seed cached data first (base + translation) so cache-only path returns 200
    _seed_entry_and_optional_translation(test_user_data["email"], "hello")

    # Generate dictionary entry
    request_data = {
        "term": "hello",
    }

    response = await client.post("/dictionary_entry/generate", json=request_data, headers=headers)
    assert response.status_code == 200

    result = cast(dict[str, object], response.json())
    assert "dictionary_entry" in result
    assert "r_user_dictionary_entry" in result

    # Verify entry structure
    dictionary_entry_data = cast(dict[str, object], result["dictionary_entry"])
    entry = cast(dict[str, object], dictionary_entry_data["json_data"])
    assert cast(str, entry["headword"]) == "hello"
    assert "source_language" in entry
    assert "meanings" in entry
    meanings = cast(list[dict[str, object]], entry["meanings"])
    assert len(meanings) > 0

    # Verify user-dictionary entry association
    user_entry_data = cast(dict[str, object], result["r_user_dictionary_entry"])
    assert "auth_user_id" in user_entry_data
    assert "dictionary_entry_id" in user_entry_data
    assert "id" in user_entry_data
    assert "created_at" in user_entry_data
    assert "updated_at" in user_entry_data


@pytest.mark.asyncio
async def test_generate_dictionary_entry_cached(
    client: AsyncClient, test_user_data: TestUserData
) -> None:
    """Test that repeated calls use cached data."""
    # Get auth token
    token = await get_auth_token(client, test_user_data)
    headers = {"Authorization": f"Bearer {token}"}

    # Seed cached data first (base + translation)
    _seed_entry_and_optional_translation(test_user_data["email"], "test")

    # Generate dictionary entry first time
    request_data = {
        "term": "test",
    }

    response1 = await client.post("/dictionary_entry/generate", json=request_data, headers=headers)
    assert response1.status_code == 200
    result1 = cast(dict[str, object], response1.json())

    # Generate again with same parameters - should use cache
    response2 = await client.post("/dictionary_entry/generate", json=request_data, headers=headers)
    assert response2.status_code == 200
    result2 = cast(dict[str, object], response2.json())

    # Results should be identical
    result1_dict_entry = cast(dict[str, object], result1["dictionary_entry"])
    result1_entry = cast(dict[str, object], result1_dict_entry["json_data"])
    result2_dict_entry = cast(dict[str, object], result2["dictionary_entry"])
    result2_entry = cast(dict[str, object], result2_dict_entry["json_data"])
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

    # Seed cached data first (base + translation)
    _seed_entry_and_optional_translation(test_user_data["email"], "computer")

    # Generate dictionary entry first time
    request_data = {
        "term": "computer",
    }

    response1 = await client.post("/dictionary_entry/generate", json=request_data, headers=headers)
    assert response1.status_code == 200

    # Force regeneration
    request_data["regenerate_full"] = True  # type: ignore[typeddict-item]

    response2 = await client.post("/dictionary_entry/generate", json=request_data, headers=headers)
    assert response2.status_code == 200

    # Both should succeed but may have different results due to regeneration
    result2 = cast(dict[str, object], response2.json())
    assert (
        cast(
            str,
            cast(
                dict[str, object], cast(dict[str, object], result2["dictionary_entry"])["json_data"]
            )["headword"],
        )
        == "computer"
    )


@pytest.mark.asyncio
async def test_generate_dictionary_entry_unauthenticated(client: AsyncClient) -> None:
    """Test that unauthenticated requests are rejected."""
    request_data = {
        "term": "test",
    }

    response = await client.post("/dictionary_entry/generate", json=request_data)
    assert response.status_code == 401
