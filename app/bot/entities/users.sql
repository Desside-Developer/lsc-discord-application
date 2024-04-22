CREATE TABLE users (
    user_id VARCHAR(255) PRIMARY KEY,
    unique_id VARCHAR(255),
    username VARCHAR(255),
    balance INT,
    on_joined DATETIME,
    inventory JSON
);