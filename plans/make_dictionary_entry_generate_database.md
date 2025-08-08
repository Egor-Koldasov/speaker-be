## Task
Make `/dictionary_entry/generate` endpoint to work with database.

## Overview
It will store the generated result into the database.
Before running AI functions it will check the database and use existing data if it's already stored there. One potential case is calling the endpoint with the same parameters multiple times. Another case is calling the endpoint with the same term, but translating it to different languages, in which case `AiDictionaryEntry` data should be reused.
The endpoint should have `regenerate_full` and `regenerate_translations` parameters to force AI function call and skip using the database data.
This case enables a scenario where multiple `AiDictionatyEntry` or `AiMeaningTranslation` lists are generated with the same parameters. When desiding which one to use, the endpoint should use the one with the most recent `updated_at` timestamp.

The AI function data will be stored in json columns called `json_data`.

## Tables
`dictionary_entry` will have `id`, timestamps and `json_data` containing `AiDictionaryEntry` model. `meaning_local_id` field in `AiMeaning` should be indexed.

`r_user_dictionary_entry` will have `id`, `auth_user_id`, `dictionary_entry_id` and timestamps. Many-to-many relationship between `user` and `dictionary_entry`.

`dictionary_entry_translation` will have `id`, `dictionary_entry_id`, `translation_language`, timestamps and `json_data` containing `AiMeaningTranslation[]` model list. `meaning_local_id` field in `AiMeaningTranslation` should be indexed.


## Requirements
The endpoint should verify that all meanings have translations with proper `meaning_local_id` fields before saving.
The data saved into the database should not store foreign languages as unicode escape sequences. It should store them as proper utf-8 characters.
The implementation should include alembic migrations.
The implementation should include integration tests.