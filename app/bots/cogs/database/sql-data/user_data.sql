-- Таблица данных о пользователях с внешним ключом
CREATE TABLE IF NOT EXISTS user_data (
    data_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    image BLOB,
    text_message TEXT,
    FOREIGN KEY (user_id) REFERENCES users(user_id) -- Связь с таблицей пользователей
);
