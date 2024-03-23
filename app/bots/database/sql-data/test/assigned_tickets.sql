-- Таблица назначенных тикетов
CREATE TABLE assigned_tickets (
    assignment_id INT PRIMARY KEY,
    ticket_id INT,
    user_id INT,
    assigned_at DATETIME,
    FOREIGN KEY (ticket_id) REFERENCES tickets(ticket_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);