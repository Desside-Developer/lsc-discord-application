-- Таблица тикетов
CREATE TABLE tickets (
    ticket_id INT PRIMARY KEY,
    system_id INT,
    user_id INT,
    status ENUM('New', 'Pending', 'In Progress', 'Closed'),
    channel_id INT,
    message_id INT,
    created_at DATETIME,
    updated_at DATETIME,
    closed_at DATETIME,
    FOREIGN KEY (system_id) REFERENCES ticket_systems(system_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);