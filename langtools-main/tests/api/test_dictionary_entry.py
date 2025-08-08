"""Integration tests for dictionary entry endpoints."""

import uuid
from typing import cast

import pytest
from httpx import AsyncClient
from sqlmodel import select

from langtools.main.api.database import get_session
from langtools.main.api.models import (
    AuthUser,
    DictionaryEntry,
    RUserDictionaryEntry,
    DictionaryEntryTranslation,
    FSRS,
    RMeaningTranslationFsrs,
)
from langtools.ai.models import (
    DictionaryWorkflowResult,
    AiDictionaryEntry,
    AiMeaning,
    AiMeaningTranslation,
)
from langtools.main.fsrs.models import FSRSCardState


@pytest.fixture
def test_user_data() -> dict[str, str | bool]:
    """Test user data with unique values for parallel test execution."""
    unique_id = str(uuid.uuid4())[:8]
    return {
        "name": f"Test User {unique_id}",
        "email": f"test-{unique_id}@example.com",
        "password": f"testpassword{unique_id}",
        "is_e2e_test": True,
    }


@pytest.fixture
def sample_dictionary_workflow_result() -> DictionaryWorkflowResult:
    """Sample dictionary workflow result for testing."""
    # Create sample meanings
    meaning1 = AiMeaning(
        headword="test",
        local_id="test-1",
        canonical_form="test",
        alternate_spellings=["teste"],
        definition="A sample test word",
        part_of_speech="noun",
        pronunciation="/test/",
        morphology="singular noun",
        register="informal",
        frequency="common",
        etymology="From English test",
        difficulty_level="beginner",
        learning_priority="high",
        example_sentences=["This is a test.", "We need to test this."],
    )

    meaning2 = AiMeaning(
        headword="test",
        local_id="test-2",
        canonical_form="test",
        alternate_spellings=[],
        definition="To examine or try something",
        part_of_speech="verb",
        pronunciation="/test/",
        morphology="infinitive verb",
        register="neutral",
        frequency="very common",
        etymology="From English test",
        difficulty_level="elementary",
        learning_priority="essential",
        example_sentences=["Let's test the system.", "I will test your knowledge."],
    )

    # Create dictionary entry
    entry = AiDictionaryEntry(
        headword="test",
        source_language="en",
        meanings=[meaning1, meaning2],
    )

    # Create translations
    translation1 = AiMeaningTranslation(
        meaning_local_id="test-1",
        headword="test",
        canonical_form="test",
        translation_language="es",
        translation="prueba",
        definition="Una palabra de ejemplo para pruebas",
        part_of_speech="sustantivo",
        pronunciation="/ˈprueba/",
        pronunciation_tips="PROO-eh-ba",
        morphology="sustantivo singular",
        register="informal",
        frequency="común",
        etymology="Del inglés test",
        difficulty_level="principiante",
        learning_priority="alta",
        example_sentences_translations=["Esto es una prueba.", "Necesitamos probar esto."],
    )

    translation2 = AiMeaningTranslation(
        meaning_local_id="test-2",
        headword="test",
        canonical_form="test",
        translation_language="es",
        translation="probar, examinar",
        definition="Examinar o intentar algo",
        part_of_speech="verbo",
        pronunciation="/proˈbar/",
        pronunciation_tips="pro-BAR",
        morphology="verbo infinitivo",
        register="neutral",
        frequency="muy común",
        etymology="Del inglés test",
        difficulty_level="elemental",
        learning_priority="esencial",
        example_sentences_translations=["Probemos el sistema.", "Voy a probar tu conocimiento."],
    )

    return DictionaryWorkflowResult(
        entry=entry,
        translations=[translation1, translation2],
    )


@pytest.fixture
def invalid_dictionary_workflow_result() -> DictionaryWorkflowResult:
    """Dictionary workflow result with mismatched meaning IDs."""
    meaning = AiMeaning(
        headword="test",
        local_id="test-1",
        canonical_form="test",
        alternate_spellings=[],
        definition="A test word",
        part_of_speech="noun",
        pronunciation="/test/",
        morphology="noun",
        register="neutral",
        frequency="common",
        etymology="English",
        difficulty_level="beginner",
        learning_priority="medium",
        example_sentences=["This is a test.", "Let's run another test."],
    )

    entry = AiDictionaryEntry(
        headword="test",
        source_language="en",
        meanings=[meaning],
    )

    # Translation with wrong meaning_local_id
    translation = AiMeaningTranslation(
        meaning_local_id="wrong-id",  # This doesn't match "test-1"
        headword="test",
        canonical_form="test",
        translation_language="es",
        translation="prueba",
        definition="Una prueba",
        part_of_speech="sustantivo",
        pronunciation="/ˈprueba/",
        pronunciation_tips="PROO-eh-ba",
        morphology="sustantivo",
        register="neutral",
        frequency="común",
        etymology="Del inglés",
        difficulty_level="principiante",
        learning_priority="medio",
        example_sentences_translations=["Esto es una prueba.", "Hagamos otra prueba."],
    )

    return DictionaryWorkflowResult(
        entry=entry,
        translations=[translation],
    )


async def authenticate_user(client: AsyncClient, test_user_data: dict[str, str | bool]) -> str:
    """Helper to register and authenticate a user, returning the access token."""
    # Register user
    await client.post("/auth/register", json=test_user_data)

    # Login to get token
    login_data = {
        "username": test_user_data["email"],
        "password": test_user_data["password"],
    }
    response = await client.post("/auth/login", data=login_data)
    login_response: dict[str, str] = cast(dict[str, str], response.json())
    return login_response["access_token"]


@pytest.mark.asyncio
async def test_create_dictionary_entry_success(
    client: AsyncClient,
    test_user_data: dict[str, str | bool],
    sample_dictionary_workflow_result: DictionaryWorkflowResult,
) -> None:
    """Test successful dictionary entry creation."""
    # Authenticate user
    token = await authenticate_user(client, test_user_data)

    # Create dictionary entry
    headers = {"Authorization": f"Bearer {token}"}
    response = await client.post(
        "/dictionary_entry",
        json=sample_dictionary_workflow_result.model_dump(),
        headers=headers,
    )

    assert response.status_code == 200
    data: dict[str, str] = cast(dict[str, str], response.json())
    assert "id" in data
    assert "json_data" in data
    assert "created_at" in data

    # Verify database records were created
    dictionary_entry_id = data["id"]

    with get_session() as session:
        # Check dictionary_entry
        dict_entry = session.get(DictionaryEntry, dictionary_entry_id)
        assert dict_entry is not None
        assert dict_entry.json_data is not None

        # Check user-dictionary relationship
        user_stmt = select(AuthUser).where(AuthUser.email == test_user_data["email"])
        user = session.exec(user_stmt).first()
        assert user is not None

        rel_stmt = select(RUserDictionaryEntry).where(
            RUserDictionaryEntry.auth_user_id == user.id,
            RUserDictionaryEntry.dictionary_entry_id == dictionary_entry_id,
        )
        relationship = session.exec(rel_stmt).first()
        assert relationship is not None

        # Check translations
        trans_stmt = select(DictionaryEntryTranslation).where(
            DictionaryEntryTranslation.dictionary_entry_id == dictionary_entry_id
        )
        translations = list(session.exec(trans_stmt).all())
        assert len(translations) == 1  # One language (Spanish)

        translation = translations[0]
        assert translation.translation_language == "es"
        assert translation.json_data is not None
        assert len(translation.json_data) == 2  # Two meanings

        # Check FSRS records
        fsrs_stmt = (
            select(FSRS)
            .join(RMeaningTranslationFsrs)
            .where(RMeaningTranslationFsrs.dictionary_entry_translation_id == translation.id)
        )
        fsrs_records = list(session.exec(fsrs_stmt).all())
        assert len(fsrs_records) == 2  # One FSRS record per meaning

        for fsrs in fsrs_records:
            assert fsrs.state == FSRSCardState.LEARNING
            assert fsrs.step == 0
            assert fsrs.reps == 0
            assert fsrs.lapses == 0
            assert fsrs.stability is None
            assert fsrs.difficulty is None

        # Check meaning-FSRS relationships
        rel_stmt = select(RMeaningTranslationFsrs).where(
            RMeaningTranslationFsrs.dictionary_entry_translation_id == translation.id
        )
        meaning_fsrs_rels = list(session.exec(rel_stmt).all())
        assert len(meaning_fsrs_rels) == 2

        meaning_ids = {rel.meaning_local_id for rel in meaning_fsrs_rels}
        assert meaning_ids == {"test-1", "test-2"}


@pytest.mark.asyncio
async def test_create_dictionary_entry_unauthenticated(
    client: AsyncClient,
    sample_dictionary_workflow_result: DictionaryWorkflowResult,
) -> None:
    """Test dictionary entry creation without authentication."""
    response = await client.post(
        "/dictionary_entry",
        json=sample_dictionary_workflow_result.model_dump(),
    )

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_create_dictionary_entry_invalid_token(
    client: AsyncClient,
    sample_dictionary_workflow_result: DictionaryWorkflowResult,
) -> None:
    """Test dictionary entry creation with invalid token."""
    headers = {"Authorization": "Bearer invalid_token"}
    response = await client.post(
        "/dictionary_entry",
        json=sample_dictionary_workflow_result.model_dump(),
        headers=headers,
    )

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_create_dictionary_entry_invalid_meaning_ids(
    client: AsyncClient,
    test_user_data: dict[str, str | bool],
    invalid_dictionary_workflow_result: DictionaryWorkflowResult,
) -> None:
    """Test dictionary entry creation with mismatched meaning IDs."""
    # Authenticate user
    token = await authenticate_user(client, test_user_data)

    # Try to create dictionary entry with invalid data
    headers = {"Authorization": f"Bearer {token}"}
    response = await client.post(
        "/dictionary_entry",
        json=invalid_dictionary_workflow_result.model_dump(),
        headers=headers,
    )

    assert response.status_code == 400
    error_response: dict[str, str] = cast(dict[str, str], response.json())
    assert "Invalid meaning translations" in error_response["detail"]
    assert "Meaning IDs mismatch" in error_response["detail"]


@pytest.mark.asyncio
async def test_create_dictionary_entry_multiple_languages(
    client: AsyncClient,
    test_user_data: dict[str, str | bool],
) -> None:
    """Test dictionary entry creation with multiple translation languages."""
    # Create workflow result with multiple languages
    meaning = AiMeaning(
        headword="hello",
        local_id="hello-1",
        canonical_form="hello",
        alternate_spellings=[],
        definition="A greeting",
        part_of_speech="interjection",
        pronunciation="/həˈloʊ/",
        morphology="interjection",
        register="neutral",
        frequency="very common",
        etymology="English greeting",
        difficulty_level="beginner",
        learning_priority="essential",
        example_sentences=["Hello, how are you?", "Hello there, friend!"],
    )

    entry = AiDictionaryEntry(
        headword="hello",
        source_language="en",
        meanings=[meaning],
    )

    # Spanish translation
    spanish_translation = AiMeaningTranslation(
        meaning_local_id="hello-1",
        headword="hello",
        canonical_form="hello",
        translation_language="es",
        translation="hola",
        definition="Un saludo",
        part_of_speech="interjección",
        pronunciation="/ˈola/",
        pronunciation_tips="OH-la",
        morphology="interjección",
        register="neutral",
        frequency="muy común",
        etymology="Saludo en inglés",
        difficulty_level="principiante",
        learning_priority="esencial",
        example_sentences_translations=["Hola, ¿cómo estás?", "¡Hola amigo!"],
    )

    # French translation
    french_translation = AiMeaningTranslation(
        meaning_local_id="hello-1",
        headword="hello",
        canonical_form="hello",
        translation_language="fr",
        translation="bonjour",
        definition="Une salutation",
        part_of_speech="interjection",
        pronunciation="/bonˈʒuʁ/",
        pronunciation_tips="bon-ZHOOR",
        morphology="interjection",
        register="neutral",
        frequency="très commun",
        etymology="Salutation anglaise",
        difficulty_level="débutant",
        learning_priority="essentiel",
        example_sentences_translations=["Bonjour, comment allez-vous?", "Bonjour mon ami!"],
    )

    workflow_result = DictionaryWorkflowResult(
        entry=entry,
        translations=[spanish_translation, french_translation],
    )

    # Authenticate user
    token = await authenticate_user(client, test_user_data)

    # Create dictionary entry
    headers = {"Authorization": f"Bearer {token}"}
    response = await client.post(
        "/dictionary_entry",
        json=workflow_result.model_dump(),
        headers=headers,
    )

    assert response.status_code == 200
    data: dict[str, str] = cast(dict[str, str], response.json())
    dictionary_entry_id = data["id"]

    # Verify multiple language translations were created
    with get_session() as session:
        trans_stmt = select(DictionaryEntryTranslation).where(
            DictionaryEntryTranslation.dictionary_entry_id == dictionary_entry_id
        )
        translations = list(session.exec(trans_stmt).all())
        assert len(translations) == 2  # Two languages

        languages = {trans.translation_language for trans in translations}
        assert languages == {"es", "fr"}

        # Each translation should have one meaning
        for trans in translations:
            assert len(trans.json_data) == 1

        # Check FSRS records - should be one per language
        total_fsrs = 0
        for trans in translations:
            rel_stmt = select(RMeaningTranslationFsrs).where(
                RMeaningTranslationFsrs.dictionary_entry_translation_id == trans.id
            )
            meaning_fsrs_rels = list(session.exec(rel_stmt).all())
            total_fsrs += len(meaning_fsrs_rels)

        assert total_fsrs == 2  # One FSRS record per translation language


@pytest.mark.asyncio
async def test_create_dictionary_entry_empty_translations(
    client: AsyncClient,
    test_user_data: dict[str, str | bool],
) -> None:
    """Test dictionary entry creation with empty translations list."""
    meaning = AiMeaning(
        headword="test",
        local_id="test-1",
        canonical_form="test",
        alternate_spellings=[],
        definition="A test",
        part_of_speech="noun",
        pronunciation="/test/",
        morphology="noun",
        register="neutral",
        frequency="common",
        etymology="English",
        difficulty_level="beginner",
        learning_priority="medium",
        example_sentences=["This is a test.", "Let's run another test."],
    )

    entry = AiDictionaryEntry(
        headword="test",
        source_language="en",
        meanings=[meaning],
    )

    workflow_result = DictionaryWorkflowResult(
        entry=entry,
        translations=[],  # Empty translations
    )

    # Authenticate user
    token = await authenticate_user(client, test_user_data)

    # Try to create dictionary entry
    headers = {"Authorization": f"Bearer {token}"}
    response = await client.post(
        "/dictionary_entry",
        json=workflow_result.model_dump(),
        headers=headers,
    )

    assert response.status_code == 400
    error_response: dict[str, str] = cast(dict[str, str], response.json())
    assert "Invalid meaning translations" in error_response["detail"]
