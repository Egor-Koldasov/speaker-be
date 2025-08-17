# Unstructured archived plans

## Store `is_e2e_test` in `auth_user` table

## Add endpoint data structure guidance to AI instructions

Use flat models. Use DB table as is, except cases with private data. Design tables to keep private data in separate tables.

## `/generate` endpoint should return db table rows in the response.
`dictionary_entry`, `dictionary_entry_translation`, `r_user_dictionary_entry`.

## Use timezone aware datetimes everywhere
Refactor the main package to use timezone aware datetime type everywhere

## Draft training prompts

### Assess language level by the current vocabulary

- Get the list of the latest due words. Items have all the data.

## Create datetime MCP tool

## Don't require review time in MCP tools
