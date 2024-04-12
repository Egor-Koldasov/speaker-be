-- +goose Up
-- +goose StatementBegin
CREATE TABLE user_info(
  id text PRIMARY KEY,
  name text NOT NULL
);

CREATE TABLE user_auth(
  id text PRIMARY KEY,
  user_id text REFERENCES user_info(id),
  token text NOT NULL UNIQUE
);

ALTER TABLE word
  ADD COLUMN user_id text REFERENCES user_info(id);

-- +goose StatementEnd
-- +goose Down
-- +goose StatementBegin
SELECT
  'down SQL query';

-- +goose StatementEnd
