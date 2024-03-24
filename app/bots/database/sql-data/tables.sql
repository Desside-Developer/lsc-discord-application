CREATE TABLE users (
    user_id VARCHAR(255) PRIMARY KEY,
    unique_id VARCHAR(255),
    username VARCHAR(255),
    balance INT,
    on_joined DATETIME,
    inventory JSON
);

CREATE TABLE tags_users (
    user_id VARCHAR(255),
    name_second VARCHAR(255),
    data_register DATETIME,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);


CREATE TABLE tickets (
    ticket_id VARCHAR(255) PRIMARY KEY,
    user_id VARCHAR(255),
    status ENUM('New', 'In Progress', 'Closed'),
    channel_id VARCHAR(255),
    message_id VARCHAR(255),
    created_at DATETIME,
    closed_at DATETIME NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);
CREATE TABLE assigned_tickets (
    assignment_id VARCHAR(255),
    ticket_id VARCHAR(255),
    user_id VARCHAR(255),
    assigned_at DATETIME,
    FOREIGN KEY (ticket_id) REFERENCES tickets(ticket_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);