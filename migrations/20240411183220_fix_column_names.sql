-- +goose Up
-- +goose StatementBegin
ALTER TABLE history_ai RENAME COLUMN operationJson TO operation_json;

ALTER TABLE history_ai RENAME COLUMN responseJson TO response_json;

-- +goose StatementEnd
-- +goose Down
-- +goose StatementBegin
SELECT
  'down SQL query';

-- +goose StatementEnd
