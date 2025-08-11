"""Integration tests for FSRS endpoints."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import TypedDict, cast

import pytest
from httpx import AsyncClient

from langtools.ai.models import AiDictionaryEntry, AiMeaning, AiMeaningTranslation
from langtools.main.api.database import get_session
from langtools.main.api.pg_queries import dictionary as dictionary_queries


class TestUserData(TypedDict):
    name: str
    email: str
    password: str
    is_e2e_test: bool


def _make_ai_entry(term: str, source_language: str = "en") -> AiDictionaryEntry:
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


def _seed_entry_and_translation_for_user(user_email: str, term: str, lang: str) -> None:
    from langtools.main.api.pg_queries.auth_user import find_auth_user_by_email

    auth_user = find_auth_user_by_email(user_email)
    assert auth_user is not None

    with get_session() as session:
        ai_entry = _make_ai_entry(term)
        entry = dictionary_queries.create_dictionary_entry(session, auth_user.id, ai_entry)
        ai_translations = _make_ai_translations(ai_entry, lang)
        dictionary_queries.create_dictionary_translation(session, entry.id, lang, ai_translations)
        session.commit()


async def _get_auth_token(client: AsyncClient, test_user_data: TestUserData) -> str:
    await client.post("/auth/register", json=test_user_data)
    login_data = {"username": test_user_data["email"], "password": test_user_data["password"]}
    response = await client.post("/auth/login", data=login_data)
    assert response.status_code == 200
    token_response = cast(dict[str, str], response.json())
    return token_response["access_token"]


@pytest.mark.asyncio
async def test_fsrs_flow_create_list_review(
    client: AsyncClient, test_user_data: TestUserData
) -> None:
    token = await _get_auth_token(client, test_user_data)
    headers = {"Authorization": f"Bearer {token}"}

    # Seed dictionary data
    term = "hello-fsrs"
    lang = "en"
    _seed_entry_and_translation_for_user(test_user_data["email"], term, lang)

    # Get translation id and a meaning_local_id
    from langtools.main.api.pg_queries.auth_user import find_auth_user_by_email
    from langtools.main.api.pg_queries.dictionary import (
        find_latest_dictionary_entry_for_user,
        find_latest_translation_for_entry,
    )

    auth_user = find_auth_user_by_email(test_user_data["email"])
    assert auth_user is not None

    with get_session() as session:
        entry = find_latest_dictionary_entry_for_user(session, auth_user.id, term)
        assert entry is not None
        translation = find_latest_translation_for_entry(session, entry.id, lang)
        assert translation is not None
        translations = translation.get_ai_meaning_translations()
        assert len(translations) > 0
        meaning_local_id = translations[0].meaning_local_id
        det_id = translation.id

    # Create FSRS
    create_payload = {
        "dictionary_entry_translation_id": det_id,
        "meaning_local_id": meaning_local_id,
    }
    create_resp = await client.post("/fsrs", json=create_payload, headers=headers)
    assert create_resp.status_code == 200
    fsrs_id = cast(dict[str, str], create_resp.json())["id"]

    # List FSRS
    list_resp = await client.get("/fsrs", headers=headers)
    assert list_resp.status_code == 200
    items = cast(list[dict[str, object]], list_resp.json())
    assert any(cast(str, item["fsrs_id"]) == fsrs_id for item in items)

    # Process a review
    review_payload = {
        "rating": 3,  # GOOD
        "review_time": datetime.now(timezone.utc).isoformat(),
    }
    review_resp = await client.post(
        f"/fsrs/{fsrs_id}/process_review", json=review_payload, headers=headers
    )
    assert review_resp.status_code == 200
    updated = cast(dict[str, object], review_resp.json())
    assert cast(str, updated["id"]) == fsrs_id
    assert updated["due"]

    # Repeat same timestamp to ensure no TZ subtraction errors
    review_resp2 = await client.post(
        f"/fsrs/{fsrs_id}/process_review", json=review_payload, headers=headers
    )
    assert review_resp2.status_code == 200
