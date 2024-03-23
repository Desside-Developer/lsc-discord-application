-- Таблица товаров
CREATE TABLE items (
    item_id INT PRIMARY KEY,
    name VARCHAR(255),
    description TEXT,
    cost INT,
    stock INT
);