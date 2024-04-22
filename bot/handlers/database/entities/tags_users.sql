CREATE TABLE tags_users (
    user_id VARCHAR(255),
    name_second VARCHAR(255),
    data_register DATETIME,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);