ALTER TABLE
    chat_messages
ADD
    COLUMN application TEXT;

CREATE INDEX chat_messages_application ON chat_messages (application);