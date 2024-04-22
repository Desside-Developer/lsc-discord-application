-- Таблица истории покупок
CREATE TABLE purchase_history (
    purchase_id INT PRIMARY KEY,
    user_id INT,
    item_id INT,
    quantity INT,
    timestamp DATETIME,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (item_id) REFERENCES items(item_id)
);