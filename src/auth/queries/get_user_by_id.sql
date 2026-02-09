-- name: get_user_by_id
SELECT user_id, username, password_hash, email, is_active, created_at
FROM users
WHERE user_id = %(user_id)s;
