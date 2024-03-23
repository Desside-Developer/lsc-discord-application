-- Таблица систем тикетов
CREATE TABLE ticket_systems (
    system_id INT PRIMARY KEY,
    name VARCHAR(255),
    description TEXT,
    max_open_tickets INT,
    category VARCHAR(255)
);