CREATE TABLE assigned_tickets (
    assignment_id VARCHAR(255),
    ticket_id VARCHAR(255),
    user_id VARCHAR(255),
    assigned_at DATETIME,
    FOREIGN KEY (ticket_id) REFERENCES tickets(ticket_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);