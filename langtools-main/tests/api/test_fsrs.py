"""Integration tests for FSRS endpoints."""

from datetime import datetime
from pathlib import Path
from typing import AsyncIterator, TypedDict, cast

import pytest
from httpx import ASGITransport, AsyncClient

from alembic import command
from alembic.config import Config
from langtools.ai.models import AiDictionaryEntry, AiMeaning, AiMeaningTranslation
from langtools.main.api.app import app
from langtools.main.api.database import get_session
from langtools.main.api.pg_queries import dictionary as dictionary_queries
from langtools.main.api.pg_queries.auth_user import find_auth_user_by_email


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


async def get_auth_token(client: AsyncClient, test_user_data: "TestUserData") -> str:
    """Register a user and return an auth token."""
    await client.post("/auth/register", json=test_user_data)
    login_data = {
        "username": test_user_data["email"],
        "password": test_user_data["password"],
    }
    response = await client.post("/auth/login", data=login_data)
    assert response.status_code == 200
    token_response = cast(dict[str, str], response.json())
    return token_response["access_token"]


class TestUserData(TypedDict):
    name: str
    email: str
    password: str
    is_e2e_test: bool


# Override client fixture for this module to call the in-process ASGI app,
# ensuring FSRS endpoints are always available during tests.
@pytest.fixture
async def client() -> AsyncIterator[AsyncClient]:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test", timeout=10.0) as ac:
        yield ac


@pytest.fixture(scope="module", autouse=True)
def migrate_db() -> None:
    """Ensure database schema is up to date for FSRS tests."""
    # Use project-level alembic.ini
    project_root = Path(__file__).resolve().parents[2]
    alembic_ini = project_root / "alembic.ini"
    cfg = Config(str(alembic_ini))
    command.upgrade(cfg, "heads")


def _seed_entry_and_translation(
    user_email: str, term: str, translation_language: str
) -> tuple[str, str]:
    """Seed base entry and translation, return (entry_id, translation_id)."""
    auth_user = find_auth_user_by_email(user_email)
    assert auth_user is not None

    with get_session() as session:
        existing_entry = dictionary_queries.find_latest_dictionary_entry_for_user(
            session, auth_user.id, term
        )
        if existing_entry:
            entry = existing_entry
            ai_entry = existing_entry.get_ai_dictionary_entry()
        else:
            ai_entry = _make_ai_entry(term)
            entry = dictionary_queries.create_dictionary_entry(session, auth_user.id, ai_entry)
        ai_translations = _make_ai_translations(ai_entry, translation_language)
        translation = dictionary_queries.create_dictionary_translation(
            session, entry.id, translation_language, ai_translations
        )
        session.commit()
        return entry.id, translation.id


@pytest.mark.asyncio
async def test_create_and_list_fsrs(client: AsyncClient, test_user_data: TestUserData) -> None:
    """Create FSRS, then list and verify sorting/payload."""
    token = await get_auth_token(client, test_user_data)
    headers = {"Authorization": f"Bearer {token}"}

    term = "alpha"
    _, translation_id = _seed_entry_and_translation(test_user_data["email"], term, "en")

    # Create FSRS for first meaning id
    create_req = {
        "dictionary_entry_translation_id": translation_id,
        "meaning_local_id": f"{term}-1",
    }
    resp_create = await client.post("/fsrs", json=create_req, headers=headers)
    assert resp_create.status_code == 200
    created = cast(dict[str, object], resp_create.json())
    fsrs_id = cast(str, created["id"])
    assert created["training"]
    assert created["dictionary_entry"]
    assert created["dictionary_entry_translation"]

    # List FSRS
    resp_list = await client.get("/fsrs", headers=headers)
    assert resp_list.status_code == 200
    items = cast(list[dict[str, object]], resp_list.json())
    assert any(cast(str, it["id"]) == fsrs_id for it in items)


@pytest.mark.asyncio
async def test_create_duplicate_fsrs_returns_error(
    client: AsyncClient, test_user_data: TestUserData
) -> None:
    token = await get_auth_token(client, test_user_data)
    headers = {"Authorization": f"Bearer {token}"}

    term = "beta"
    _, translation_id = _seed_entry_and_translation(test_user_data["email"], term, "en")

    create_req = {
        "dictionary_entry_translation_id": translation_id,
        "meaning_local_id": f"{term}-1",
    }
    resp1 = await client.post("/fsrs", json=create_req, headers=headers)
    assert resp1.status_code == 200

    resp2 = await client.post("/fsrs", json=create_req, headers=headers)
    assert resp2.status_code == 400


@pytest.mark.asyncio
async def test_process_review_flow(client: AsyncClient, test_user_data: TestUserData) -> None:
    token = await get_auth_token(client, test_user_data)
    headers = {"Authorization": f"Bearer {token}"}

    term = "gamma"
    _, translation_id = _seed_entry_and_translation(test_user_data["email"], term, "en")

    create_req = {
        "dictionary_entry_translation_id": translation_id,
        "meaning_local_id": f"{term}-1",
    }
    resp_create = await client.post("/fsrs", json=create_req, headers=headers)
    assert resp_create.status_code == 200
    created = cast(dict[str, object], resp_create.json())
    fsrs_id = cast(str, created["id"])

    # Process review with GOOD
    review_req = {"rating": 3, "review_time": datetime.now().isoformat()}
    resp_review = await client.post(
        f"/fsrs/{fsrs_id}/process_review", json=review_req, headers=headers
    )
    assert resp_review.status_code == 200
    updated = cast(dict[str, object], resp_review.json())
    training = cast(dict[str, object], updated["training"])
    assert cast(int, training["reps"]) == 1


@pytest.mark.asyncio
async def test_list_sorted_by_due(client: AsyncClient, test_user_data: TestUserData) -> None:
    """Verify list is sorted by due date ascending."""
    token = await get_auth_token(client, test_user_data)
    headers = {"Authorization": f"Bearer {token}"}

    # Seed two distinct terms & translations
    term1, term2 = "sorta", "sortb"
    _, tr1 = _seed_entry_and_translation(test_user_data["email"], term1, "en")
    _, tr2 = _seed_entry_and_translation(test_user_data["email"], term2, "en")

    # Create two FSRS records
    for tr, term in [(tr1, term1), (tr2, term2)]:
        resp = await client.post(
            "/fsrs",
            json={
                "dictionary_entry_translation_id": tr,
                "meaning_local_id": f"{term}-1",
            },
            headers=headers,
        )
        assert resp.status_code == 200

    # Process one to push due further into future (so the other stays earlier)
    resp_list_before = await client.get("/fsrs", headers=headers)
    items_before = cast(list[dict[str, object]], resp_list_before.json())
    assert len(items_before) >= 2

    latest = items_before[-1]
    review_req = {"rating": 4, "review_time": datetime.now().isoformat()}
    await client.post(f"/fsrs/{latest['id']}/process_review", json=review_req, headers=headers)

    # Verify sorted by due ascending
    resp_list_after = await client.get("/fsrs", headers=headers)
    items = cast(list[dict[str, object]], resp_list_after.json())
    dues = [cast(dict[str, object], it["training"]) for it in items]
    due_times = [datetime.fromisoformat(cast(str, d["due"])) for d in dues]
    assert due_times == sorted(due_times)
