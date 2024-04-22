CREATE TABLE transactions (
    transaction_id INT PRIMARY KEY,
    sender_id INT,
    receiver_id INT,
    amount INT,
    timestamp DATETIME,
    FOREIGN KEY (sender_id) REFERENCES users(user_id),
    FOREIGN KEY (receiver_id) REFERENCES users(user_id)
);