"""Tests for dictionary endpoints."""

import uuid
from typing import cast

import pytest
from httpx import AsyncClient

from langtools.ai.models import (
    AiDictionaryEntry,
    AiMeaning,
    AiMeaningTranslation,
)
from langtools.main.api.schemas.dictionary import (
    AddDictionaryEntryResponse,
    DictionaryEntryResponse,
    DictionaryEntryListResponse,
    DictionaryEntryFSRSResponse,
)


@pytest.fixture
def sample_dictionary_entry() -> AiDictionaryEntry:
    """Create a sample dictionary entry for testing."""
    return AiDictionaryEntry(
        headword="test",
        source_language="en",
        meanings=[
            AiMeaning(
                headword="test",
                local_id="test-1",
                canonical_form="test",
                alternate_spellings=[],
                definition="A procedure to establish quality or reliability",
                part_of_speech="noun",
                pronunciation="/test/",
                morphology="regular",
                register="formal",
                frequency="common",
                etymology="From Latin testum",
                difficulty_level="intermediate",
                learning_priority="high",
                example_sentences=[
                    "The students took a test.",
                    "We need to test this hypothesis.",
                ],
            )
        ],
    )


@pytest.fixture
def sample_translations() -> list[AiMeaningTranslation]:
    """Create sample translations for testing."""
    return [
        AiMeaningTranslation(
            meaning_local_id="test-1",
            headword="test",
            canonical_form="test",
            translation_language="es",
            translation="prueba, examen",
            definition="Un procedimiento para establecer calidad o confiabilidad",
            part_of_speech="sustantivo",
            pronunciation="/test/",
            pronunciation_tips="Se pronuncia como 'test'",
            morphology="regular",
            register="formal",
            frequency="común",
            etymology="Del latín testum",
            difficulty_level="intermedio",
            learning_priority="alta",
            example_sentences_translations=[
                "Los estudiantes tomaron un examen.",
                "Necesitamos probar esta hipótesis.",
            ],
        )
    ]


@pytest.fixture
def test_dict_user_data() -> dict[str, str | bool]:
    """Test user data for dictionary tests."""
    unique_id = str(uuid.uuid4())[:8]
    return {
        "name": f"Dict Test User {unique_id}",
        "email": f"dict-test-{unique_id}@example.com",
        "password": f"testpassword{unique_id}",
        "is_e2e_test": True,
    }


@pytest.mark.asyncio
async def test_add_dictionary_entry(
    client: AsyncClient,
    test_dict_user_data: dict[str, str | bool],
    sample_dictionary_entry: AiDictionaryEntry,
    sample_translations: list[AiMeaningTranslation],
) -> None:
    """Test adding a dictionary entry."""
    # Register and login user
    await client.post("/auth/register", json=test_dict_user_data)

    login_data = {
        "username": test_dict_user_data["email"],
        "password": test_dict_user_data["password"],
    }
    login_response = await client.post("/auth/login", data=login_data)
    token = cast(dict[str, str], login_response.json())["access_token"]

    # Add dictionary entry with authentication
    headers = {"Authorization": f"Bearer {token}"}
    request_data = {
        "entry": sample_dictionary_entry.model_dump(),
        "translations": [trans.model_dump() for trans in sample_translations],
    }

    response = await client.post("/dictionary_entry", json=request_data, headers=headers)
    assert response.status_code == 200

    result = AddDictionaryEntryResponse.model_validate(response.json())
    assert result.dictionary_entry_id
    assert isinstance(result.dictionary_entry_id, str)
    assert len(result.dictionary_entry_id) > 0


@pytest.mark.asyncio
async def test_add_dictionary_entry_missing_translations(
    client: AsyncClient,
    test_dict_user_data: dict[str, str | bool],
    sample_dictionary_entry: AiDictionaryEntry,
) -> None:
    """Test adding a dictionary entry with missing translations."""
    # Register and login user
    await client.post("/auth/register", json=test_dict_user_data)

    login_data = {
        "username": test_dict_user_data["email"],
        "password": test_dict_user_data["password"],
    }
    login_response = await client.post("/auth/login", data=login_data)
    token = cast(dict[str, str], login_response.json())["access_token"]

    # Add dictionary entry with missing translations
    headers = {"Authorization": f"Bearer {token}"}
    request_data = {
        "entry": sample_dictionary_entry.model_dump(),
        "translations": [],  # Missing translations
    }

    response = await client.post("/dictionary_entry", json=request_data, headers=headers)
    assert response.status_code == 400
    assert "Translation validation failed" in response.json()["detail"]


@pytest.mark.asyncio
async def test_add_dictionary_entry_extra_translations(
    client: AsyncClient,
    test_dict_user_data: dict[str, str | bool],
    sample_dictionary_entry: AiDictionaryEntry,
    sample_translations: list[AiMeaningTranslation],
) -> None:
    """Test adding a dictionary entry with extra translations."""
    # Register and login user
    await client.post("/auth/register", json=test_dict_user_data)

    login_data = {
        "username": test_dict_user_data["email"],
        "password": test_dict_user_data["password"],
    }
    login_response = await client.post("/auth/login", data=login_data)
    token = cast(dict[str, str], login_response.json())["access_token"]

    # Add extra translation with non-existent meaning_local_id
    extra_translation = AiMeaningTranslation(
        meaning_local_id="test-2",  # This doesn't exist in our sample entry
        headword="extra",
        canonical_form="extra",
        translation_language="es",
        translation="extra",
        definition="Extra translation",
        part_of_speech="noun",
        pronunciation="/extra/",
        pronunciation_tips="Extra",
        morphology="regular",
        register="formal",
        frequency="common",
        etymology="Extra",
        difficulty_level="intermediate",
        learning_priority="medium",
        example_sentences_translations=["Extra example 1", "Extra example 2"],
    )

    headers = {"Authorization": f"Bearer {token}"}
    request_data = {
        "entry": sample_dictionary_entry.model_dump(),
        "translations": [trans.model_dump() for trans in sample_translations + [extra_translation]],
    }

    response = await client.post("/dictionary_entry", json=request_data, headers=headers)
    assert response.status_code == 400
    assert "Translation validation failed" in response.json()["detail"]


@pytest.mark.asyncio
async def test_add_dictionary_entry_unauthenticated(
    client: AsyncClient,
    sample_dictionary_entry: AiDictionaryEntry,
    sample_translations: list[AiMeaningTranslation],
) -> None:
    """Test adding a dictionary entry without authentication."""
    request_data = {
        "entry": sample_dictionary_entry.model_dump(),
        "translations": [trans.model_dump() for trans in sample_translations],
    }

    response = await client.post("/dictionary_entry", json=request_data)
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_get_dictionary_entry(
    client: AsyncClient,
    test_dict_user_data: dict[str, str | bool],
    sample_dictionary_entry: AiDictionaryEntry,
    sample_translations: list[AiMeaningTranslation],
) -> None:
    """Test getting a dictionary entry by ID."""
    # Register and login user
    await client.post("/auth/register", json=test_dict_user_data)

    login_data = {
        "username": test_dict_user_data["email"],
        "password": test_dict_user_data["password"],
    }
    login_response = await client.post("/auth/login", data=login_data)
    token = cast(dict[str, str], login_response.json())["access_token"]

    # Add a dictionary entry first
    headers = {"Authorization": f"Bearer {token}"}
    request_data = {
        "entry": sample_dictionary_entry.model_dump(),
        "translations": [trans.model_dump() for trans in sample_translations],
    }

    add_response = await client.post("/dictionary_entry", json=request_data, headers=headers)
    entry_id = cast(dict[str, str], add_response.json())["dictionary_entry_id"]

    # Get the dictionary entry
    get_response = await client.get(f"/dictionary_entry/{entry_id}", headers=headers)
    assert get_response.status_code == 200

    result = DictionaryEntryResponse.model_validate(get_response.json())
    assert result.id == entry_id
    assert result.entry.headword == sample_dictionary_entry.headword


@pytest.mark.asyncio
async def test_get_dictionary_entry_not_found(
    client: AsyncClient,
    test_dict_user_data: dict[str, str | bool],
) -> None:
    """Test getting a non-existent dictionary entry."""
    # Register and login user
    await client.post("/auth/register", json=test_dict_user_data)

    login_data = {
        "username": test_dict_user_data["email"],
        "password": test_dict_user_data["password"],
    }
    login_response = await client.post("/auth/login", data=login_data)
    token = cast(dict[str, str], login_response.json())["access_token"]

    # Try to get non-existent entry
    headers = {"Authorization": f"Bearer {token}"}
    response = await client.get("/dictionary_entry/non-existent-id", headers=headers)
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_list_dictionary_entries(
    client: AsyncClient,
    test_dict_user_data: dict[str, str | bool],
    sample_dictionary_entry: AiDictionaryEntry,
    sample_translations: list[AiMeaningTranslation],
) -> None:
    """Test listing user's dictionary entries."""
    # Register and login user
    await client.post("/auth/register", json=test_dict_user_data)

    login_data = {
        "username": test_dict_user_data["email"],
        "password": test_dict_user_data["password"],
    }
    login_response = await client.post("/auth/login", data=login_data)
    token = cast(dict[str, str], login_response.json())["access_token"]

    # Add a dictionary entry first
    headers = {"Authorization": f"Bearer {token}"}
    request_data = {
        "entry": sample_dictionary_entry.model_dump(),
        "translations": [trans.model_dump() for trans in sample_translations],
    }

    await client.post("/dictionary_entry", json=request_data, headers=headers)

    # List entries
    list_response = await client.get("/dictionary_entry", headers=headers)
    assert list_response.status_code == 200

    result = DictionaryEntryListResponse.model_validate(list_response.json())
    assert result.total >= 1
    assert len(result.entries) >= 1
    assert result.entries[0].headword == sample_dictionary_entry.headword


@pytest.mark.asyncio
async def test_list_dictionary_entries_pagination(
    client: AsyncClient,
    test_dict_user_data: dict[str, str | bool],
) -> None:
    """Test pagination in dictionary entries list."""
    # Register and login user
    await client.post("/auth/register", json=test_dict_user_data)

    login_data = {
        "username": test_dict_user_data["email"],
        "password": test_dict_user_data["password"],
    }
    login_response = await client.post("/auth/login", data=login_data)
    token = cast(dict[str, str], login_response.json())["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # List with pagination params
    list_response = await client.get("/dictionary_entry?page=1&page_size=5", headers=headers)
    assert list_response.status_code == 200

    result = DictionaryEntryListResponse.model_validate(list_response.json())
    assert result.page == 1
    assert result.page_size == 5


@pytest.mark.asyncio
async def test_get_dictionary_entry_fsrs(
    client: AsyncClient,
    test_dict_user_data: dict[str, str | bool],
    sample_dictionary_entry: AiDictionaryEntry,
    sample_translations: list[AiMeaningTranslation],
) -> None:
    """Test getting FSRS data for dictionary entry."""
    # Register and login user
    await client.post("/auth/register", json=test_dict_user_data)

    login_data = {
        "username": test_dict_user_data["email"],
        "password": test_dict_user_data["password"],
    }
    login_response = await client.post("/auth/login", data=login_data)
    token = cast(dict[str, str], login_response.json())["access_token"]

    # Add a dictionary entry first
    headers = {"Authorization": f"Bearer {token}"}
    request_data = {
        "entry": sample_dictionary_entry.model_dump(),
        "translations": [trans.model_dump() for trans in sample_translations],
    }

    add_response = await client.post("/dictionary_entry", json=request_data, headers=headers)
    entry_id = cast(dict[str, str], add_response.json())["dictionary_entry_id"]

    # Get FSRS data
    fsrs_response = await client.get(f"/dictionary_entry/{entry_id}/fsrs", headers=headers)
    assert fsrs_response.status_code == 200

    result = DictionaryEntryFSRSResponse.model_validate(fsrs_response.json())
    assert result.dictionary_entry_id == entry_id
    assert len(result.meanings_fsrs) == len(sample_dictionary_entry.meanings)


@pytest.mark.asyncio
async def test_update_dictionary_entry(
    client: AsyncClient,
    test_dict_user_data: dict[str, str | bool],
    sample_dictionary_entry: AiDictionaryEntry,
    sample_translations: list[AiMeaningTranslation],
) -> None:
    """Test updating a dictionary entry."""
    # Register and login user
    await client.post("/auth/register", json=test_dict_user_data)

    login_data = {
        "username": test_dict_user_data["email"],
        "password": test_dict_user_data["password"],
    }
    login_response = await client.post("/auth/login", data=login_data)
    token = cast(dict[str, str], login_response.json())["access_token"]

    # Add a dictionary entry first
    headers = {"Authorization": f"Bearer {token}"}
    request_data = {
        "entry": sample_dictionary_entry.model_dump(),
        "translations": [trans.model_dump() for trans in sample_translations],
    }

    add_response = await client.post("/dictionary_entry", json=request_data, headers=headers)
    entry_id = cast(dict[str, str], add_response.json())["dictionary_entry_id"]

    # Update the entry
    updated_entry = sample_dictionary_entry.model_copy(deep=True)
    updated_entry.meanings[0].definition = "Updated definition"

    update_data = {
        "entry": updated_entry.model_dump(),
        "translations": [trans.model_dump() for trans in sample_translations],
    }

    update_response = await client.put(
        f"/dictionary_entry/{entry_id}", json=update_data, headers=headers
    )
    assert update_response.status_code == 200

    # Verify the update
    get_response = await client.get(f"/dictionary_entry/{entry_id}", headers=headers)
    result = DictionaryEntryResponse.model_validate(get_response.json())
    assert result.entry.meanings[0].definition == "Updated definition"


@pytest.mark.asyncio
async def test_update_dictionary_entry_not_found(
    client: AsyncClient,
    test_dict_user_data: dict[str, str | bool],
    sample_dictionary_entry: AiDictionaryEntry,
    sample_translations: list[AiMeaningTranslation],
) -> None:
    """Test updating a non-existent dictionary entry."""
    # Register and login user
    await client.post("/auth/register", json=test_dict_user_data)

    login_data = {
        "username": test_dict_user_data["email"],
        "password": test_dict_user_data["password"],
    }
    login_response = await client.post("/auth/login", data=login_data)
    token = cast(dict[str, str], login_response.json())["access_token"]

    # Try to update non-existent entry
    headers = {"Authorization": f"Bearer {token}"}
    update_data = {
        "entry": sample_dictionary_entry.model_dump(),
        "translations": [trans.model_dump() for trans in sample_translations],
    }

    response = await client.put(
        "/dictionary_entry/non-existent-id", json=update_data, headers=headers
    )
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_update_meaning_fsrs(
    client: AsyncClient,
    test_dict_user_data: dict[str, str | bool],
    sample_dictionary_entry: AiDictionaryEntry,
    sample_translations: list[AiMeaningTranslation],
) -> None:
    """Test updating FSRS data for a meaning."""
    # Register and login user
    await client.post("/auth/register", json=test_dict_user_data)

    login_data = {
        "username": test_dict_user_data["email"],
        "password": test_dict_user_data["password"],
    }
    login_response = await client.post("/auth/login", data=login_data)
    token = cast(dict[str, str], login_response.json())["access_token"]

    # Add a dictionary entry first
    headers = {"Authorization": f"Bearer {token}"}
    request_data = {
        "entry": sample_dictionary_entry.model_dump(),
        "translations": [trans.model_dump() for trans in sample_translations],
    }

    add_response = await client.post("/dictionary_entry", json=request_data, headers=headers)
    entry_id = cast(dict[str, str], add_response.json())["dictionary_entry_id"]

    # Get FSRS data to find meaning_fsrs_id
    fsrs_response = await client.get(f"/dictionary_entry/{entry_id}/fsrs", headers=headers)
    fsrs_result = DictionaryEntryFSRSResponse.model_validate(fsrs_response.json())
    meaning_fsrs_id = fsrs_result.meanings_fsrs[0].meaning_fsrs_id

    # Update FSRS data (simulate review)
    from datetime import datetime, timezone

    review_data = {
        "rating": 3,  # Good rating
        "review_time": datetime.now(timezone.utc).isoformat(),
    }

    update_response = await client.put(
        f"/dictionary_entry/{entry_id}/fsrs/{meaning_fsrs_id}", json=review_data, headers=headers
    )
    assert update_response.status_code == 200
