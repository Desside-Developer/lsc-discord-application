-- Таблица ролей
CREATE TABLE IF NOT EXISTS roles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    role_id VARCHAR(255) NOT NULL,
    role_name VARCHAR(255) NOT NULL
);
