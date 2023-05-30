CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    user_token TEXT NOT NULL
);

CREATE TYPE MessageType AS ENUM ('human', 'jelly', 'tool');

CREATE TABLE chat_messages (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    message_type MessageType NOT NULL,
    content TEXT NOT NULL,
    timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    FOREIGN KEY (user_id) REFERENCES users (user_id)
);

CREATE INDEX chat_messages_user_id ON chat_messages(user_id);

CREATE INDEX chat_messages_timestamp ON chat_messages(timestamp);

CREATE UNIQUE INDEX users_user_token ON users(user_token);