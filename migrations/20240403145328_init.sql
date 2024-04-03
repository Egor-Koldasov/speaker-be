-- +goose Up
-- +goose StatementBegin
CREATE TABLE IF NOT EXISTS word(
  num serial PRIMARY KEY,
  json jsonb
);

-- +goose StatementEnd
-- +goose Down
-- +goose StatementBegin
SELECT
  'down SQL query';

-- +goose StatementEnd
