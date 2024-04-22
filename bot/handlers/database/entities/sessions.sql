CREATE TABLE IF NOT EXISTS sessions (
  session_id TEXT UNIQUE,
  token TEXT,
  refresh_token TEXT,
  token_expires_at TIMESTAMP,
  user_id BIGINT PRIMARY KEY
);