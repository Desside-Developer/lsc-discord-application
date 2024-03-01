CREATE TABLE IF NOT EXISTS tickets (
    id SERIAL PRIMARY KEY,
    chat_id VARCHAR(255) NOT NULL,
    message_id_control_panel VARCHAR(255) NOT NULL,
    message_id VARCHAR(255) NOT NULL,
    user_name VARCHAR(255) NOT NULL,
    user_id BIGINT UNSIGNED NOT NULL,
    user_moderator_id BIGINT UNSIGNED NOT NULL,
    user_moderator_name VARCHAR(255) NOT NULL,
    INDEX idx_user_id (user_id),
    INDEX idx_user_moderator_id (user_moderator_id)
);