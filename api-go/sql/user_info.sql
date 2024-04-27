-- name: GetUserInfo :one
SELECT
  *
FROM
  user_info
WHERE
  id = $1;

