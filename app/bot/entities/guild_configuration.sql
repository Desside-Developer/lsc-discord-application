CREATE TABLE guild_configuration (
    id INT AUTO_INCREMENT PRIMARY KEY,
    guild_id BIGINT UNIQUE,
    prefix VARCHAR(255) DEFAULT '?',
    welcome_channel_id VARCHAR(255)
);