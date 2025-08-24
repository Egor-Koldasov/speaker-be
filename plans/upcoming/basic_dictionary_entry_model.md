# Increase the speed of the AI generation by removing everything non-essential from AI output.

- Remove everything non-essential from `AiMeaning` model.

- Remove `AiMeaningTranslation` completely.

## 1. Remove everything non-essential from `AiMeaning` model.

## 2. Create a migration script to make fsrs records relate to `dictionary_entry` instead of `dictionary_entry_translation`.

## 3. Update the API to use new models.

- Generate only the minimal data first.

### Postponed for later

- Generate the extended data in a background.

- Generate the translations in a background.
