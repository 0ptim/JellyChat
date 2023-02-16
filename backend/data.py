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
            question TEXT NOT NULL,
            answer TEXT NOT NULL,
            rating INTEGER NOT NULL,
            CHECK (rating >= 0 AND rating <= 1)
        )
        ''')
        db.commit()


def add_rating(question: str, answer: str, rating: int):
    """Add a rating to the database.

    Args:
        question: The question that was asked.
        answer: The answer that was selected.
        rating: The rating of the answer. 0 = bad, 1 = good.
    """
    with get_db() as db:
        db.execute('INSERT INTO ratings (question, answer, rating) VALUES (?, ?, ?)',
                   (question, answer, rating))
        db.commit()
