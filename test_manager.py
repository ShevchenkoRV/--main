
from database import conn, cursor


class TestManager:
    def __init__(self):
        self.conn   = conn
        self.cursor = cursor


    def get_tests(self):

        cursor.execute("SELECT id, title FROM tests")
        return cursor.fetchall()

    def add_test(self, title):

        cursor.execute("INSERT INTO tests (title) VALUES (?)", (title,))
        conn.commit()
        return cursor.lastrowid

    def delete_test(self, test_id):

        cursor.execute("DELETE FROM questions WHERE test_id = ?", (test_id,))
        cursor.execute("DELETE FROM tests WHERE id = ?", (test_id,))
        conn.commit()

    def get_questions(self, test_id):

        cursor.execute("SELECT * FROM questions WHERE test_id = ?", (test_id,))
        return cursor.fetchall()

    def add_question(self, test_id, question, answer1, answer2,
                     answer3, answer4, correct_answer):

        cursor.execute("""
            INSERT INTO questions
                (test_id, question, answer1, answer2, answer3, answer4, correct_answer)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (test_id, question, answer1, answer2, answer3, answer4, correct_answer))
        conn.commit()

    def update_question(self, question_id, question, answer1, answer2,
                        answer3, answer4, correct_answer):

        cursor.execute("""
            UPDATE questions
            SET question = ?, answer1 = ?, answer2 = ?,
                answer3 = ?, answer4 = ?, correct_answer = ?
            WHERE id = ?
        """, (question, answer1, answer2, answer3, answer4, correct_answer, question_id))
        conn.commit()

    def delete_question(self, question_id):

        cursor.execute("DELETE FROM questions WHERE id = ?", (question_id,))
        conn.commit()


    def save_result(self, student_name, test_id, score):

        cursor.execute("""
            INSERT INTO results (student_name, test_id, score)
            VALUES (?, ?, ?)
        """, (student_name, test_id, score))
        conn.commit()

    def get_all_students(self):

        cursor.execute(
            "SELECT DISTINCT student_name FROM results ORDER BY student_name"
        )
        return [row[0] for row in cursor.fetchall() if row[0]]

    def get_results_for_student(self, student_name):

        cursor.execute("""
            SELECT t.title, r.score
            FROM results r
            JOIN tests t ON r.test_id = t.id
            WHERE r.student_name = ?
            ORDER BY r.id DESC
        """, (student_name,))
        return cursor.fetchall()
