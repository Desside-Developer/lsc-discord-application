-- Таблица ответов тикета
CREATE TABLE ticket_answers (
    answer_id INT PRIMARY KEY,
    ticket_id INT,
    user_id INT,
    answer_text TEXT,
    created_at DATETIME,
    FOREIGN KEY (ticket_id) REFERENCES tickets(ticket_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);