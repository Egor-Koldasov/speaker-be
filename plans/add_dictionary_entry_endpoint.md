Add a new endpoint to the API.
Endpoint POST `/dictionary_entry`.

It will accept the same models as in `DictionaryWorkflowResult` and it will store them in the database.

The models will store this data in json columns called `json_data`.

`dictionary_entry` will have `id`, timestamps and `json_data` containing `AiDictionaryEntry` model. `meaning_local_id` field in `AiMeaning` should be indexed.

`r_user_dictionary_entry` will have `id`, `auth_user_id`, `dictionary_entry_id` and timestamps. Many-to-many relationship between `user` and `dictionary_entry`.

`dictionary_entry_translation` will have `id`, `dictionary_entry_id`, `translation_language`, timestamps and `json_data` containing `AiMeaningTranslation[]` model list. `meaning_local_id` field in `AiMeaningTranslation` should be indexed.

`fsrs` will have `id`, timestamps and all fields from `FSRSTrainingData` model as separate columns.

`r_meaning_translation_fsrs` will have `id`, `dictionary_entry_translation_id`, `meaning_local_id`, timestamps. One-to-many relationship between `dictionary_entry_translation` and `fsrs`. Virtually one-to-one relationship between fsrs and an individual `AiMeaningTranslation` by `meaning_local_id`.

The endpoint should verify that all meanings have translations with proper `meaning_local_id` fields before saving. Then save into all four tables.
