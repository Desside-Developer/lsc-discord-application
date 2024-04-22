CREATE TABLE tickets (
    ticket_id VARCHAR(255) PRIMARY KEY,
    user_id VARCHAR(255),
    status ENUM('New', 'In Progress', 'Closed'),
    channel_id VARCHAR(255),
    message_id VARCHAR(255),
    created_at DATETIME,
    closed_at DATETIME NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
)