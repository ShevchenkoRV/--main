import ttkbootstrap as ttk
from tkinter import messagebox

from .base_frame import BaseFrame
from config import STYLE


class TestTaking(BaseFrame):

    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        self.test_id      = None
        self.test_name    = ""
        self.student_name = ""
        self.questions    = []
        self.current_index = 0
        self.user_answers  = []  # список списків: [[0, 2], [1], ...]

        self._build_ui()

    def _build_ui(self):
        container = ttk.Frame(self)
        container.pack(expand=True, fill="both", padx=100, pady=30)

        # Лічильник "Питання X з Y"
        self.counter_label = ttk.Label(
            container,
            text="",
            font=STYLE["fonts"]["default"],
            bootstyle="secondary"
        )
        self.counter_label.pack(anchor="w", pady=(0, 5))

        # Текст питання
        self.question_label = ttk.Label(
            container,
            text="",
            font=STYLE["fonts"]["header"],
            wraplength=900,
            justify="left"
        )
        self.question_label.pack(anchor="w", pady=(0, 20))

        # Варіанти відповідей (чекбокси)
        answers_area = ttk.Frame(container)
        answers_area.pack(fill="x", pady=10)

        self.answer_checkboxes = []
        self.answer_vars       = []

        for _ in range(4):
            var = ttk.IntVar()
            checkbox = ttk.Checkbutton(
                answers_area,
                text="",
                variable=var,
                bootstyle="primary",
                style="LargeToggle.TCheckbutton"
            )
            checkbox.pack(anchor="w", pady=5, fill="x")
            self.answer_vars.append(var)
            self.answer_checkboxes.append(checkbox)

        # Кнопки "Далі" і "Скасувати"
        buttons_row = ttk.Frame(container)
        buttons_row.pack(pady=30, anchor="w")

        ttk.Button(
            buttons_row,
            text="Далі →",
            bootstyle="primary",
            width=20,
            command=self._next_question
        ).pack(side="left", padx=(0, 10), ipady=5)

        ttk.Button(
            buttons_row,
            text="Скасувати",
            bootstyle="secondary",
            width=15,
            command=self._cancel_test
        ).pack(side="left", ipady=5)


    def on_show(self, test_name=None, student_name=None, **kwargs):
        """Знаходить тест у БД і розпочинає проходження."""
        self.test_name    = test_name    or ""
        self.student_name = student_name or ""

        # Знаходимо id тесту за назвою
        self.test_id = None
        for tid, tname in self.test_manager.get_tests():
            if tname == test_name:
                self.test_id = tid
                break

        if self.test_id is None:
            messagebox.showerror("Помилка", f"Тест '{test_name}' не знайдено!")
            self.controller.show_frame("StudentMenu")
            return

        self.questions     = self.test_manager.get_questions(self.test_id)
        self.current_index = 0
        self.user_answers  = []

        self._show_current_question()


    def _show_current_question(self):

        if self.current_index >= len(self.questions):
            self._finish_test()
            return

        question = self.questions[self.current_index]

        self.counter_label.config(
            text=f"Питання {self.current_index + 1} з {len(self.questions)}"
        )
        self.question_label.config(text=question[2])

        # Скидаємо вибір і оновлюємо текст варіантів
        for i, checkbox in enumerate(self.answer_checkboxes):
            self.answer_vars[i].set(0)
            checkbox.config(text=f"  {question[3 + i]}")

    def _next_question(self):

        selected_indices = [i for i, v in enumerate(self.answer_vars) if v.get() == 1]
        self.user_answers.append(selected_indices)
        self.current_index += 1
        self._show_current_question()

    def _finish_test(self):

        self.controller.show_frame(
            "ResultsScreen",
            test_name=self.test_name,
            student_name=self.student_name,
            questions=self.questions,
            user_answers=self.user_answers,
            test_id=self.test_id,
        )

    def _cancel_test(self):
        confirmed = messagebox.askyesno("Скасування", "Вийти з тесту? Прогрес не збережеться.")
        if confirmed:
            self.controller.show_frame("StudentMenu")
