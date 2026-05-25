
import sqlite3
import os

DB_FILE = "testing_system.db"

print(f"База даних: {os.path.abspath(DB_FILE)}")

conn   = sqlite3.connect(DB_FILE)
cursor = conn.cursor()


# Таблиця тестів
cursor.execute("""
    CREATE TABLE IF NOT EXISTS tests (
        id    INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL
    )
""")


cursor.execute("""
    CREATE TABLE IF NOT EXISTS questions (
        id             INTEGER PRIMARY KEY AUTOINCREMENT,
        test_id        INTEGER NOT NULL,
        question       TEXT NOT NULL,
        answer1        TEXT NOT NULL,
        answer2        TEXT NOT NULL,
        answer3        TEXT NOT NULL,
        answer4        TEXT NOT NULL,
        correct_answer TEXT NOT NULL,
        FOREIGN KEY (test_id) REFERENCES tests(id)
    )
""")

# Таблиця результатів студентів
cursor.execute("""
    CREATE TABLE IF NOT EXISTS results (
        id           INTEGER PRIMARY KEY AUTOINCREMENT,
        student_name TEXT,
        test_id      INTEGER,
        score        INTEGER
    )
""")

conn.commit()
