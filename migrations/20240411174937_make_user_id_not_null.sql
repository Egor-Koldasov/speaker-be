-- +goose Up
-- +goose StatementBegin
ALTER TABLE user_auth
  ALTER COLUMN user_id SET NOT NULL;

ALTER TABLE word
  ALTER COLUMN user_id SET NOT NULL;

ALTER TABLE text_history
  ALTER COLUMN user_id SET NOT NULL;

ALTER TABLE word_history
  ALTER COLUMN user_id SET NOT NULL;

-- +goose StatementEnd
-- +goose Down
-- +goose StatementBegin
SELECT
  'down SQL query';

-- +goose StatementEnd
