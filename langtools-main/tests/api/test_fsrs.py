"""Integration tests for FSRS spaced repetition endpoints."""

from datetime import datetime, timezone
from typing import TypedDict, cast

import pytest
from httpx import AsyncClient

from langtools.ai import AiDictionaryEntry, AiMeaning, AiMeaningTranslation
from langtools.main.fsrs import Rating

# DB setup helpers
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
        alternate_spellings=[],
        definition=f"Definition of {term}",
        part_of_speech="noun",
        semantic_field=None,
        pronunciation="/term/",
        tone_notation=None,
        syllable_count=None,
        phonetic_variations=None,
        morphology="N/A",
        register="neutral",
        frequency="common",
        etymology="N/A",
        difficulty_level="beginner",
        learning_priority="essential",
        common_mistakes=None,
        mnemonic_hints=None,
        practice_suggestions=None,
        example_sentences=[f"{term} example 1.", f"{term} example 2."],
        collocations=None,
        synonyms=None,
        antonyms=None,
    )
    return AiDictionaryEntry(headword=term, source_language=source_language, meanings=[meaning])


def _make_ai_translations(
    entry: AiDictionaryEntry, translation_language: str
) -> list[AiMeaningTranslation]:
    """Create minimal valid translations for each meaning in entry."""
    translations: list[AiMeaningTranslation] = []
    for m in entry.meanings:
        translations.append(
            AiMeaningTranslation(
                meaning_local_id=m.local_id,
                headword=m.headword,
                canonical_form=f"{m.canonical_form}-{translation_language}",
                translation_language=translation_language,
                translation=f"{m.headword}-{translation_language}",
                definition=f"Translation of {m.headword} to {translation_language}",
                part_of_speech=m.part_of_speech,
                semantic_field=None,
                pronunciation="/tr/",
                pronunciation_tips="Tip",
                tone_notation=None,
                tone_tips=None,
                morphology="N/A",
                register="neutral",
                frequency="common",
                etymology="N/A",
                difficulty_level="beginner",
                learning_priority="essential",
                common_mistakes=None,
                mnemonic_hints=None,
                practice_suggestions=None,
                example_sentences_translations=[
                    f"{m.headword} {translation_language} ex1",
                    f"{m.headword} {translation_language} ex2",
                ],
                collocations=None,
            )
        )
    return translations


def _seed_dictionary_data(user_email: str, term: str, translation_language: str) -> tuple[str, str]:
    """Seed dictionary entry and translation data.

    Returns entry_translation_id and meaning_local_id.
    """
    auth_user = find_auth_user_by_email(user_email)
    assert auth_user is not None

    with get_session() as session:
        # Create dictionary entry
        ai_entry = _make_ai_entry(term)
        entry = dictionary_queries.create_dictionary_entry(session, auth_user.id, ai_entry)

        # Create translation
        ai_translations = _make_ai_translations(ai_entry, translation_language)
        translation = dictionary_queries.create_dictionary_translation(
            session, entry.id, translation_language, ai_translations
        )

        session.commit()

        # Return translation ID and first meaning's meaning_local_id for FSRS creation
        return translation.id, ai_translations[0].meaning_local_id


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
async def test_create_fsrs_record_basic(client: AsyncClient, test_user_data: TestUserData) -> None:
    """Test basic FSRS record creation."""
    # Get auth token
    token = await get_auth_token(client, test_user_data)
    headers = {"Authorization": f"Bearer {token}"}

    # Seed dictionary data
    translation_id, meaning_local_id = _seed_dictionary_data(test_user_data["email"], "hello", "es")

    # Create FSRS record
    request_data = {
        "dictionary_entry_translation_id": translation_id,
        "meaning_local_id": meaning_local_id,
    }

    response = await client.post("/fsrs", json=request_data, headers=headers)
    assert response.status_code == 200

    result = cast(dict[str, object], response.json())
    assert "fsrs_id" in result
    assert "due" in result
    assert "stability" in result
    assert "difficulty" in result
    assert "state" in result
    assert "step" in result
    assert "reps" in result
    assert "lapses" in result

    # Check initial values for new card
    assert cast(int, result["reps"]) == 0
    assert cast(int, result["lapses"]) == 0
    assert cast(int, result["state"]) == 1  # LEARNING state


@pytest.mark.asyncio
async def test_create_fsrs_record_duplicate(
    client: AsyncClient, test_user_data: TestUserData
) -> None:
    """Test that creating duplicate FSRS record returns error."""
    # Get auth token
    token = await get_auth_token(client, test_user_data)
    headers = {"Authorization": f"Bearer {token}"}

    # Seed dictionary data
    translation_id, meaning_local_id = _seed_dictionary_data(test_user_data["email"], "test", "fr")

    # Create FSRS record
    request_data = {
        "dictionary_entry_translation_id": translation_id,
        "meaning_local_id": meaning_local_id,
    }

    # First creation should succeed
    response1 = await client.post("/fsrs", json=request_data, headers=headers)
    assert response1.status_code == 200

    # Second creation should fail
    response2 = await client.post("/fsrs", json=request_data, headers=headers)
    assert response2.status_code == 409
    assert "already exists" in response2.json()["detail"]


@pytest.mark.asyncio
async def test_create_fsrs_record_invalid_meaning(
    client: AsyncClient, test_user_data: TestUserData
) -> None:
    """Test creating FSRS record with invalid meaning translation."""
    # Get auth token
    token = await get_auth_token(client, test_user_data)
    headers = {"Authorization": f"Bearer {token}"}

    # Seed dictionary data
    translation_id, _ = _seed_dictionary_data(test_user_data["email"], "word", "de")

    # Try to create FSRS record with invalid meaning_local_id
    request_data = {
        "dictionary_entry_translation_id": translation_id,
        "meaning_local_id": "nonexistent-meaning-id",
    }

    response = await client.post("/fsrs", json=request_data, headers=headers)
    assert response.status_code == 400
    assert "not found" in response.json()["detail"]


@pytest.mark.asyncio
async def test_create_fsrs_record_nonexistent_translation(
    client: AsyncClient, test_user_data: TestUserData
) -> None:
    """Test creating FSRS record with nonexistent translation ID."""
    # Get auth token
    token = await get_auth_token(client, test_user_data)
    headers = {"Authorization": f"Bearer {token}"}

    # Try to create FSRS record with nonexistent translation ID
    request_data = {
        "dictionary_entry_translation_id": "nonexistent-translation-id",
        "meaning_local_id": "any-meaning-id",
    }

    response = await client.post("/fsrs", json=request_data, headers=headers)
    assert response.status_code == 400
    assert "not found" in response.json()["detail"]


@pytest.mark.asyncio
async def test_create_fsrs_record_unauthenticated(client: AsyncClient) -> None:
    """Test that unauthenticated requests are rejected."""
    request_data = {
        "dictionary_entry_translation_id": "some-id",
        "meaning_local_id": "some-meaning-id",
    }

    response = await client.post("/fsrs", json=request_data)
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_process_review_basic(client: AsyncClient, test_user_data: TestUserData) -> None:
    """Test basic review processing."""
    # Get auth token
    token = await get_auth_token(client, test_user_data)
    headers = {"Authorization": f"Bearer {token}"}

    # Seed dictionary data and create FSRS record
    translation_id, meaning_local_id = _seed_dictionary_data(test_user_data["email"], "study", "ja")

    # Create FSRS record
    create_response = await client.post(
        "/fsrs",
        json={
            "dictionary_entry_translation_id": translation_id,
            "meaning_local_id": meaning_local_id,
        },
        headers=headers,
    )
    assert create_response.status_code == 200
    create_result = cast(dict[str, object], create_response.json())
    fsrs_id = cast(str, create_result["fsrs_id"])

    # Process a review with GOOD rating
    review_time = datetime.now(timezone.utc)
    review_data = {
        "rating": Rating.GOOD.value,
        "review_time": review_time.isoformat(),
    }

    response = await client.post(
        f"/fsrs/{fsrs_id}/process_review", json=review_data, headers=headers
    )
    assert response.status_code == 200

    result = cast(dict[str, object], response.json())
    assert cast(str, result["fsrs_id"]) == fsrs_id
    assert cast(int, result["reps"]) == 1  # Should increment
    assert cast(int, result["lapses"]) == 0  # Should not increment for GOOD rating
    assert result["last_review"] is not None


@pytest.mark.asyncio
async def test_process_review_failed_card(
    client: AsyncClient, test_user_data: TestUserData
) -> None:
    """Test processing review with AGAIN rating (failed card)."""
    # Get auth token
    token = await get_auth_token(client, test_user_data)
    headers = {"Authorization": f"Bearer {token}"}

    # Seed dictionary data and create FSRS record
    translation_id, meaning_local_id = _seed_dictionary_data(
        test_user_data["email"], "difficult", "ko"
    )

    # Create FSRS record
    create_response = await client.post(
        "/fsrs",
        json={
            "dictionary_entry_translation_id": translation_id,
            "meaning_local_id": meaning_local_id,
        },
        headers=headers,
    )
    assert create_response.status_code == 200
    create_result = cast(dict[str, object], create_response.json())
    fsrs_id = cast(str, create_result["fsrs_id"])

    # Process a review with AGAIN rating
    review_time = datetime.now(timezone.utc)
    review_data = {
        "rating": Rating.AGAIN.value,
        "review_time": review_time.isoformat(),
    }

    response = await client.post(
        f"/fsrs/{fsrs_id}/process_review", json=review_data, headers=headers
    )
    assert response.status_code == 200

    result = cast(dict[str, object], response.json())
    assert cast(int, result["reps"]) == 1  # Should increment
    assert cast(int, result["lapses"]) == 1  # Should increment for AGAIN rating


@pytest.mark.asyncio
async def test_process_review_invalid_rating(
    client: AsyncClient, test_user_data: TestUserData
) -> None:
    """Test processing review with invalid rating."""
    # Get auth token
    token = await get_auth_token(client, test_user_data)
    headers = {"Authorization": f"Bearer {token}"}

    # Seed dictionary data and create FSRS record
    translation_id, meaning_local_id = _seed_dictionary_data(test_user_data["email"], "test", "zh")

    # Create FSRS record
    create_response = await client.post(
        "/fsrs",
        json={
            "dictionary_entry_translation_id": translation_id,
            "meaning_local_id": meaning_local_id,
        },
        headers=headers,
    )
    assert create_response.status_code == 200
    create_result = cast(dict[str, object], create_response.json())
    fsrs_id = cast(str, create_result["fsrs_id"])

    # Try to process review with invalid rating
    review_time = datetime.now(timezone.utc)
    review_data = {
        "rating": 0,  # Invalid rating (should be 1-4)
        "review_time": review_time.isoformat(),
    }

    response = await client.post(
        f"/fsrs/{fsrs_id}/process_review", json=review_data, headers=headers
    )
    assert response.status_code == 422  # Pydantic validation error


@pytest.mark.asyncio
async def test_process_review_nonexistent_fsrs(
    client: AsyncClient, test_user_data: TestUserData
) -> None:
    """Test processing review for nonexistent FSRS record."""
    # Get auth token
    token = await get_auth_token(client, test_user_data)
    headers = {"Authorization": f"Bearer {token}"}

    # Try to process review for nonexistent FSRS record
    review_time = datetime.now(timezone.utc)
    review_data = {
        "rating": Rating.GOOD.value,
        "review_time": review_time.isoformat(),
    }

    response = await client.post(
        "/fsrs/nonexistent-id/process_review", json=review_data, headers=headers
    )
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_process_review_access_denied(
    client: AsyncClient, test_user_data: TestUserData
) -> None:
    """Test that users cannot process reviews for other users' records."""
    # Create first user and FSRS record
    token1 = await get_auth_token(client, test_user_data)
    headers1 = {"Authorization": f"Bearer {token1}"}

    translation_id, meaning_local_id = _seed_dictionary_data(
        test_user_data["email"], "private", "it"
    )

    create_response = await client.post(
        "/fsrs",
        json={
            "dictionary_entry_translation_id": translation_id,
            "meaning_local_id": meaning_local_id,
        },
        headers=headers1,
    )
    assert create_response.status_code == 200
    create_result = cast(dict[str, object], create_response.json())
    fsrs_id = cast(str, create_result["fsrs_id"])

    # Create second user
    test_user_data2: TestUserData = {
        "name": "Test User 2",
        "email": "test2@example.com",
        "password": "testpass123",
        "is_e2e_test": True,
    }
    token2 = await get_auth_token(client, test_user_data2)
    headers2 = {"Authorization": f"Bearer {token2}"}

    # Try to process review with second user's token
    review_time = datetime.now(timezone.utc)
    review_data = {
        "rating": Rating.GOOD.value,
        "review_time": review_time.isoformat(),
    }

    response = await client.post(
        f"/fsrs/{fsrs_id}/process_review", json=review_data, headers=headers2
    )
    assert response.status_code == 403
    assert "Access denied" in response.json()["detail"]


@pytest.mark.asyncio
async def test_get_fsrs_records_empty(client: AsyncClient, test_user_data: TestUserData) -> None:
    """Test getting FSRS records when user has none."""
    # Get auth token
    token = await get_auth_token(client, test_user_data)
    headers = {"Authorization": f"Bearer {token}"}

    # Get FSRS records
    response = await client.get("/fsrs", headers=headers)
    assert response.status_code == 200

    result = cast(dict[str, object], response.json())
    assert cast(int, result["total"]) == 0
    assert cast(list[object], result["items"]) == []
    assert cast(int, result["page"]) == 1
    assert cast(int, result["page_size"]) == 20
    assert cast(bool, result["has_next"]) is False
    assert cast(bool, result["has_prev"]) is False


@pytest.mark.asyncio
async def test_get_fsrs_records_with_data(
    client: AsyncClient, test_user_data: TestUserData
) -> None:
    """Test getting FSRS records with data."""
    # Get auth token
    token = await get_auth_token(client, test_user_data)
    headers = {"Authorization": f"Bearer {token}"}

    # Create multiple FSRS records
    terms = ["word1", "word2", "word3"]
    for term in terms:
        translation_id, meaning_local_id = _seed_dictionary_data(
            test_user_data["email"], term, "es"
        )
        create_response = await client.post(
            "/fsrs",
            json={
                "dictionary_entry_translation_id": translation_id,
                "meaning_local_id": meaning_local_id,
            },
            headers=headers,
        )
        assert create_response.status_code == 200

    # Get FSRS records
    response = await client.get("/fsrs", headers=headers)
    assert response.status_code == 200

    result = cast(dict[str, object], response.json())
    assert cast(int, result["total"]) == 3
    items = cast(list[dict[str, object]], result["items"])
    assert len(items) == 3

    # Check structure of first item
    item = items[0]
    assert "fsrs_id" in item
    assert "due" in item
    assert "dictionary_entry" in item
    assert "dictionary_entry_translation" in item
    assert "meaning_local_id" in item

    # Verify dictionary data is included
    dictionary_entry = cast(dict[str, object], item["dictionary_entry"])
    assert "headword" in dictionary_entry
    assert "meanings" in dictionary_entry

    dictionary_translation = cast(list[dict[str, object]], item["dictionary_entry_translation"])
    assert len(dictionary_translation) > 0
    assert "meaning_local_id" in dictionary_translation[0]
    assert "translation" in dictionary_translation[0]


@pytest.mark.asyncio
async def test_get_fsrs_records_pagination(
    client: AsyncClient, test_user_data: TestUserData
) -> None:
    """Test FSRS records pagination."""
    # Get auth token
    token = await get_auth_token(client, test_user_data)
    headers = {"Authorization": f"Bearer {token}"}

    # Create 5 FSRS records
    for i in range(5):
        translation_id, meaning_local_id = _seed_dictionary_data(
            test_user_data["email"], f"term{i}", "fr"
        )
        create_response = await client.post(
            "/fsrs",
            json={
                "dictionary_entry_translation_id": translation_id,
                "meaning_local_id": meaning_local_id,
            },
            headers=headers,
        )
        assert create_response.status_code == 200

    # Get first page with page_size=3
    response = await client.get("/fsrs?page=1&page_size=3", headers=headers)
    assert response.status_code == 200

    result = cast(dict[str, object], response.json())
    assert cast(int, result["total"]) == 5
    assert len(cast(list[object], result["items"])) == 3
    assert cast(int, result["page"]) == 1
    assert cast(int, result["page_size"]) == 3
    assert cast(bool, result["has_next"]) is True
    assert cast(bool, result["has_prev"]) is False

    # Get second page
    response = await client.get("/fsrs?page=2&page_size=3", headers=headers)
    assert response.status_code == 200

    result = cast(dict[str, object], response.json())
    assert cast(int, result["total"]) == 5
    assert len(cast(list[object], result["items"])) == 2  # Remaining items
    assert cast(int, result["page"]) == 2
    assert cast(int, result["page_size"]) == 3
    assert cast(bool, result["has_next"]) is False
    assert cast(bool, result["has_prev"]) is True


@pytest.mark.asyncio
async def test_get_fsrs_records_unauthenticated(client: AsyncClient) -> None:
    """Test that unauthenticated requests are rejected."""
    response = await client.get("/fsrs")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_fsrs_workflow_end_to_end(client: AsyncClient, test_user_data: TestUserData) -> None:
    """Test complete FSRS workflow from creation to multiple reviews."""
    # Get auth token
    token = await get_auth_token(client, test_user_data)
    headers = {"Authorization": f"Bearer {token}"}

    # Seed dictionary data
    translation_id, meaning_local_id = _seed_dictionary_data(
        test_user_data["email"], "workflow", "pt"
    )

    # 1. Create FSRS record
    create_response = await client.post(
        "/fsrs",
        json={
            "dictionary_entry_translation_id": translation_id,
            "meaning_local_id": meaning_local_id,
        },
        headers=headers,
    )
    assert create_response.status_code == 200
    create_result = cast(dict[str, object], create_response.json())
    fsrs_id = cast(str, create_result["fsrs_id"])

    # Verify initial state
    assert cast(int, create_result["reps"]) == 0
    assert cast(int, create_result["lapses"]) == 0

    # 2. Process first review (GOOD)
    review_time1 = datetime.now(timezone.utc)
    review1_response = await client.post(
        f"/fsrs/{fsrs_id}/process_review",
        json={
            "rating": Rating.GOOD.value,
            "review_time": review_time1.isoformat(),
        },
        headers=headers,
    )
    assert review1_response.status_code == 200
    review1_result = cast(dict[str, object], review1_response.json())
    assert cast(int, review1_result["reps"]) == 1
    assert cast(int, review1_result["lapses"]) == 0

    # 3. Process second review (AGAIN - failed)
    review_time2 = datetime.now(timezone.utc)
    review2_response = await client.post(
        f"/fsrs/{fsrs_id}/process_review",
        json={
            "rating": Rating.AGAIN.value,
            "review_time": review_time2.isoformat(),
        },
        headers=headers,
    )
    assert review2_response.status_code == 200
    review2_result = cast(dict[str, object], review2_response.json())
    assert cast(int, review2_result["reps"]) == 2
    assert cast(int, review2_result["lapses"]) == 1

    # 4. Get FSRS records and verify the item is there with updated data
    list_response = await client.get("/fsrs", headers=headers)
    assert list_response.status_code == 200
    list_result = cast(dict[str, object], list_response.json())

    items = cast(list[dict[str, object]], list_result["items"])
    assert len(items) == 1

    item = items[0]
    assert cast(str, item["fsrs_id"]) == fsrs_id
    assert cast(int, item["reps"]) == 2
    assert cast(int, item["lapses"]) == 1
    assert item["last_review"] is not None

    # Verify complete dictionary data is included
    assert "dictionary_entry" in item
    assert "dictionary_entry_translation" in item
    assert cast(str, item["meaning_local_id"]) == meaning_local_id
