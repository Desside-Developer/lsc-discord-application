-- Таблица вопросов тикета
CREATE TABLE ticket_questions (
    question_id INT PRIMARY KEY,
    system_id INT,
    question_text TEXT,
    required BOOLEAN,
    FOREIGN KEY (system_id) REFERENCES ticket_systems(system_id)
);