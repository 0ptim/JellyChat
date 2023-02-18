import sqlite3


def get_db():
    """Opens a new database connection (or creates a new database) if there is none yet for the current application context."""
    return sqlite3.connect('database.db')


def init_db():
    """Initialize the database."""
    with get_db() as db:
        db.execute('''
        CREATE TABLE IF NOT EXISTS ratings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date DATETIME DEFAULT CURRENT_TIMESTAMP,
            question TEXT NOT NULL,
            answer TEXT NOT NULL,
            rating INTEGER DEFAULT NULL,
            CHECK (rating >= 0 AND rating <= 1)
        )
        ''')
        db.commit()


def add_QA(question: str, answer: str):
    """Add a question and answer to the database.

    Args:
        question: The question that was asked.
        answer: The answer that was selected.

    Returns:
        The id of the new entry.
    """
    with get_db() as db:
        cursor = db.cursor()
        cursor.execute('INSERT INTO ratings (question, answer) VALUES (?, ?)',
                       (question, answer))
        db.commit()
        return cursor.lastrowid


def add_rating(id: int, rating: int):
    """Add a rating to a question and answer.

    Args:
        id: The id of the question and answer.
        rating: The rating (0 or 1).
    """
    with get_db() as db:
        cursor = db.cursor()
        cursor.execute('UPDATE ratings SET rating = ? WHERE id = ?',
                       (rating, id))
        db.commit()
