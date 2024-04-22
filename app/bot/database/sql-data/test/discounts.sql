-- Таблица скидок
CREATE TABLE discounts (
    discount_id INT PRIMARY KEY,
    item_id INT,
    discount_percentage INT,
    start_date DATETIME,
    end_date DATETIME,
    FOREIGN KEY (item_id) REFERENCES items(item_id)
);