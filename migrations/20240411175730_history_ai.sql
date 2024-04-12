-- +goose Up
-- +goose StatementBegin
CREATE TABLE history_ai(
  id text PRIMARY KEY,
  user_id text REFERENCES user_info(id),
  operationJson jsonb NOT NULL,
  responseJson jsonb NOT NULL,
  created_at timestamp DEFAULT CURRENT_TIMESTAMP
);

-- +goose StatementEnd
-- +goose Down
-- +goose StatementBegin
SELECT
  'down SQL query';

-- +goose StatementEnd
