Implement endpoints to manage FSRS data.

GET `/fsrs` - return a list of fsrs records. For each fsrs record return a full `dictionary_entry_translation` and `dictionary_entry` records. It should suppport pagination and return the result sorted by `due` date, the most recent first.

POST `/fsrs/{id}/process_review` - process a review session and return updated training data. Uses `process_review` function from fsrs module. `id` should refer to `fsrs` table. The endpoint should be abstracted away from the kind of resource it refers to, in this case `dictionary_entry_translation`. It only works with fsrs data.
