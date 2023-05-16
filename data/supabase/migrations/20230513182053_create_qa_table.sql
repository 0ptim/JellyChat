CREATE TABLE QA (
    id SERIAL PRIMARY KEY,
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    question TEXT NOT NULL,
    answer TEXT NOT NULL,
    rating INTEGER DEFAULT NULL,
    CHECK (
        rating >= 0
        AND rating <= 1
    )
)