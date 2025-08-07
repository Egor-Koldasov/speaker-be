Add a new endpoint to the API.
Endpoint POST `/dictionary_entry`.

It will accept the same models as in `DictionaryWorkflowResult` and it will store them in the database.

The models will store this data in json columns called `json_data`.

`dictionary_entry` will have `id`, timestamps and `json_data` containing `AiDictionaryEntry` model.

`user_dictionary_entry` will have `id`, `auth_user_id`, `dictionary_entry_id` and timestamps. Many-to-many relationship between `user` and `dictionary_entry`.

`dictionary_entry_translation` will have `id`, `dictionary_entry_id`, timestamps and `json_data` containing `AiMeaningTranslation[]` model list.

`meaning_fsrs` will have `id`, `dictionary_entry_id`, timestamps and all fields from `FSRSTrainingData` model as separate columns.

The endpoint should verify that all meanings have translations with proper `meaning_local_id` fields before saving. Then save into all four tables.
