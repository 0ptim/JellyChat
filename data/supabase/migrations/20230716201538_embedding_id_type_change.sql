-- Change the id column type from integer to UUID after a langchain update
-- 1. Add a new column
ALTER TABLE
    langchain
ADD
    COLUMN uuid_id UUID;

-- 2. Populate the new column with UUIDs (assuming that you want to generate new UUIDs)
UPDATE
    langchain
SET
    uuid_id = uuid_generate_v4();

-- Before proceeding, make sure that the new UUIDs are unique and not null
-- 3. Drop the old id column
ALTER TABLE
    langchain DROP COLUMN id;

-- 4. Rename the new uuid_id column to id
ALTER TABLE
    langchain RENAME COLUMN uuid_id TO id;