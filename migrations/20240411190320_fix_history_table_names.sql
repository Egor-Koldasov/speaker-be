-- +goose Up
-- +goose StatementBegin
ALTER TABLE text_history RENAME TO history_text;

ALTER TABLE word_history RENAME TO history_word;

-- +goose StatementEnd
-- +goose Down
-- +goose StatementBegin
SELECT
  'down SQL query';

-- +goose StatementEnd
