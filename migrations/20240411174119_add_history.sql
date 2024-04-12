-- +goose Up
-- +goose StatementBegin
CREATE TABLE text_history(
  id text PRIMARY KEY,
  text_input text NOT NULL,
  user_id text REFERENCES user_info(id),
  created_at timestamp DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE word_history(
  id text PRIMARY KEY,
  word text NOT NULL,
  user_id text REFERENCES user_info(id),
  created_at timestamp DEFAULT CURRENT_TIMESTAMP
);

-- +goose StatementEnd
-- +goose Down
-- +goose StatementBegin
SELECT
  'down SQL query';

-- +goose StatementEnd
