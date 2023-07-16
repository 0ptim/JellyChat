ALTER TABLE
    langchain
ADD
    COLUMN uuid_id UUID;

UPDATE
    langchain
SET
    uuid_id = uuid_generate_v4();

ALTER TABLE
    langchain DROP COLUMN id;

ALTER TABLE
    langchain RENAME COLUMN uuid_id TO id;