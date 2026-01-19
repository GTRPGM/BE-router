SELECT user_id, username, password_hash, email, is_active, created_at
FROM users
WHERE username = %(username)s
  AND is_active = TRUE;
