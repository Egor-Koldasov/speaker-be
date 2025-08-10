## Task
Implement endpoints to manage FSRS data.

## Endpoints
GET `/fsrs` - return a list of fsrs records. For each fsrs record return a full `dictionary_entry_translation` and `dictionary_entry` records. It should suppport pagination and return the result sorted by `due` date, soonest due first.

POST `/fsrs` - Create a new fsrs record to add something to the learner's flashcards. Binds it to the individual `AiMeaningTranslation`. On duplicate return error.
Parameters:
- `dictionary_entry_translation_id`
- `meaning_local_id`

POST `/fsrs/{id}/process_review` - process a review session and return updated training data. Uses `process_review` function from fsrs module. `id` should refer to `fsrs` table. The endpoint should be abstracted away from the kind of resource it refers to, in this case `dictionary_entry_translation`. It only works with fsrs data.

## Tables
`fsrs` will have `id`, timestamps and all fields from `FSRSTrainingData` model as separate columns.

`fsrs` records later might support different types of resources they store the training data for. We start with one relation that matches meaning translation.
`r_meaning_translation_fsrs` will have `auth_user_id`, `fsrs_id`, `dictionary_entry_translation_id`, `meaning_local_id`, timestamps. One-to-many relationship between `dictionary_entry_translation` and `fsrs`. Virtually one-to-one relationship between fsrs and an individual `AiMeaningTranslation` by `meaning_local_id`.