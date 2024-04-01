-- Таблица категорий
CREATE TABLE categories (
    category_id INT PRIMARY KEY,
    item_id INT,
    category_name VARCHAR(255),
    FOREIGN KEY (item_id) REFERENCES items(item_id)
);