import ttkbootstrap as ttk

from .base_frame import BaseFrame
from config import STYLE

ANSWER_LABELS = ["А", "Б", "В", "Г"]


class ResultsScreen(BaseFrame):


    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        self.questions    = []
        self.user_answers = []
        self.test_name    = ""
        self.student_name = ""
        self.test_id      = None

        self._build_ui()

    def _build_ui(self):
        container = ttk.Frame(self)
        container.pack(expand=True, fill="both", padx=100, pady=30)

        self.title_label = ttk.Label(container, text="", font=STYLE["fonts"]["title"])
        self.title_label.pack(anchor="w", pady=(0, 5))

        self.student_label = ttk.Label(container, text="", font=STYLE["fonts"]["header"],
                                       bootstyle="secondary")
        self.student_label.pack(anchor="w", pady=(0, 20))

        self.score_label = ttk.Label(container, text="", font=("Helvetica", 36, "bold"))
        self.score_label.pack(anchor="w", pady=(0, 20))

        # Таблиця з детальними результатами
        table_container = ttk.Frame(container)
        table_container.pack(fill="both", expand=True)

        columns = ("num", "question", "your_answer", "correct_answer", "result")
        self.results_table = ttk.Treeview(
            table_container,
            columns=columns,
            show="headings",
            bootstyle="primary"
        )

        self.results_table.heading("num",            text="№")
        self.results_table.heading("question",       text="Питання")
        self.results_table.heading("your_answer",    text="Ваша відповідь")
        self.results_table.heading("correct_answer", text="Правильна відповідь")
        self.results_table.heading("result",         text="Результат")

        self.results_table.column("num",            width=40,  anchor="center")
        self.results_table.column("question",       width=400)
        self.results_table.column("your_answer",    width=200)
        self.results_table.column("correct_answer", width=200)
        self.results_table.column("result",         width=80,  anchor="center")

        scrollbar = ttk.Scrollbar(table_container, orient="vertical",
                                  command=self.results_table.yview, bootstyle="round-primary")
        self.results_table.configure(yscrollcommand=scrollbar.set)
        self.results_table.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Кнопки внизу
        buttons_row = ttk.Frame(container)
        buttons_row.pack(pady=20, anchor="w")

        ttk.Button(buttons_row, text="На головну", bootstyle="primary", width=20,
                   command=lambda: self.controller.show_frame("MainMenu"),
                   ).pack(side="left", padx=(0, 10), ipady=5)

        ttk.Button(buttons_row, text="Ще раз", bootstyle="secondary", width=15,
                   command=lambda: self.controller.show_frame("StudentMenu"),
                   ).pack(side="left", ipady=5)

    def on_show(self, test_name=None, student_name=None, questions=None,
                user_answers=None, test_id=None, **kwargs):
        self.test_name    = test_name    or ""
        self.student_name = student_name or ""
        self.questions    = questions    or []
        self.user_answers = user_answers or []
        self.test_id      = test_id

        self.title_label.config(text=f"Результати: {self.test_name}")
        self.student_label.config(text=f"Студент: {self.student_name}")

        score = self._fill_results_table()
        self._save_result(score)

    def _fill_results_table(self):
        for row in self.results_table.get_children():
            self.results_table.delete(row)

        correct_count = 0

        for i, question in enumerate(self.questions):
            question_text   = question[2]
            options         = question[3:7]
            correct_indices = self._parse_correct_answer(question[7] if len(question) > 7 else "0")
            user_indices    = self.user_answers[i] if i < len(self.user_answers) else []

            is_correct = set(user_indices) == set(correct_indices)
            if is_correct:
                correct_count += 1

            user_text    = self._format_answers(options, user_indices)
            correct_text = self._format_answers(options, correct_indices)

            self.results_table.insert("", "end", values=(
                i + 1,
                question_text,
                user_text,
                correct_text,
                "✔" if is_correct else "✘",
            ))

        self._update_score_label(correct_count, len(self.questions))
        return correct_count

    def _parse_correct_answer(self, raw):

        return list(map(int, raw.split(","))) if raw else []

    def _format_answers(self, options, indices):

        parts = [
            f"{ANSWER_LABELS[i]}) {options[i]}"
            for i in indices
            if i < len(options)
        ]
        return ", ".join(parts) if parts else "—"

    def _update_score_label(self, score, total):

        percent = round(score / total * 100) if total else 0

        if percent >= 90:
            style = "success"
        elif percent >= 60:
            style = "warning"
        else:
            style = "danger"

        self.score_label.config(
            text=f"{score} / {total}  ({percent}%)",
            bootstyle=style
        )

    def _save_result(self, score):

        try:

            if not self.test_id:
                for tid, tname in self.test_manager.get_tests():
                    if tname == self.test_name:
                        self.test_id = tid
                        break

            self.test_manager.save_result(self.student_name, self.test_id, score)

        except Exception as error:
            print(f"Не вдалося зберегти результат: {error}")
