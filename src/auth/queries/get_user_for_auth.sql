SELECT user_id, username, password_hash
FROM users
WHERE username = %(username)s
  AND is_active = TRUE;
