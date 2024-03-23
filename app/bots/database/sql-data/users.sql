CREATE TABLE users (
    user_id VARCHAR(255) PRIMARY KEY,
    unique_id VARCHAR(255),
    username VARCHAR(255),
    balance INT,
    on_joined DATETIME,
    inventory JSON
);

CREATE TABLE tags_users (
    user_id VARCHAR(255),
    name_second VARCHAR(255),
    data_register DATETIME,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);