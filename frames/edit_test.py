import ttkbootstrap as ttk
from tkinter import messagebox, Listbox

from .base_frame import BaseFrame
from config import STYLE


class EditTest(BaseFrame):


    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        self.current_test_id = None
        self.all_tests       = []
        self.all_questions   = []

        self._build_ui()

    def _build_ui(self):


        # Заголовок
        header = ttk.Frame(self)
        header.pack(fill="x", padx=20, pady=10)
        ttk.Label(header, text="Редагування тесту", font=STYLE["fonts"]["title"]).pack(anchor="w")

        # Основна область з трьома колонками
        main_area = ttk.Frame(self)
        main_area.pack(fill="both", expand=True, padx=20, pady=10)

        self._build_tests_column(main_area)
        self._build_questions_column(main_area)
        self._build_editor_column(main_area)

        # Кнопка "Назад"
        ttk.Button(
            self,
            text="Назад",
            bootstyle="secondary",
            command=lambda: self.controller.show_frame("AdminMenu")
        ).pack(side="bottom", pady=10)

    def _build_tests_column(self, parent):

        column = ttk.Frame(parent)
        column.pack(side="left", fill="both", expand=True, padx=(0, 10))

        ttk.Label(column, text="Оберіть тест:", font=STYLE["fonts"]["header"]).pack(anchor="w")

        self.tests_listbox = Listbox(column, height=10, font=STYLE["fonts"]["default"])
        self.tests_listbox.pack(fill="both", expand=True)
        self.tests_listbox.bind("<<ListboxSelect>>", self._on_test_selected)

        ttk.Button(
            column,
            text="Видалити тест",
            bootstyle="danger",
            command=self._delete_selected_test
        ).pack(fill="x", pady=(5, 0))

    def _build_questions_column(self, parent):

        column = ttk.Frame(parent)
        column.pack(side="left", fill="both", expand=True, padx=(0, 10))

        ttk.Label(column, text="Питання тесту:", font=STYLE["fonts"]["header"]).pack(anchor="w")

        self.questions_listbox = Listbox(column, height=10, font=STYLE["fonts"]["default"])
        self.questions_listbox.pack(fill="both", expand=True)
        self.questions_listbox.bind("<<ListboxSelect>>", self._on_question_selected)

    def _build_editor_column(self, parent):

        column = ttk.Frame(parent)
        column.pack(side="right", fill="both", expand=True)

        ttk.Label(column, text="Редагувати питання:", font=STYLE["fonts"]["header"]).pack(anchor="w")

        # Поле тексту питання
        self.question_entry = ttk.Entry(column, font=STYLE["fonts"]["default"])
        self.question_entry.pack(fill="x", pady=5)

        self.answer_entries = []
        self.correct_vars   = []

        for _ in range(4):
            row = ttk.Frame(column)
            row.pack(fill="x", pady=2)

            var = ttk.IntVar()
            ttk.Checkbutton(row, variable=var).pack(side="left")

            entry = ttk.Entry(row, font=STYLE["fonts"]["default"])
            entry.pack(side="left", fill="x", expand=True)

            self.correct_vars.append(var)
            self.answer_entries.append(entry)

        # Кнопки дій
        actions = ttk.Frame(column)
        actions.pack(fill="x", pady=10)

        ttk.Button(
            actions,
            text="Зберегти зміни",
            bootstyle="primary",
            command=self._save_question_changes
        ).pack(fill="x", pady=2)

        ttk.Button(
            actions,
            text="Видалити питання",
            bootstyle="danger",
            command=self._delete_selected_question
        ).pack(fill="x", pady=2)


    def on_show(self, **kwargs):

        self.current_test_id = None
        self.all_questions   = []
        self._load_tests()
        self.questions_listbox.delete(0, "end")
        self._clear_editor()


    def _load_tests(self):
        self.all_tests = self.test_manager.get_tests()
        self.tests_listbox.delete(0, "end")

        if not self.all_tests:
            self.tests_listbox.insert("end", "Немає тестів")
        else:
            for _, test_name in self.all_tests:
                self.tests_listbox.insert("end", test_name)

    def _load_questions(self):
        self.all_questions = self.test_manager.get_questions(self.current_test_id)
        self.questions_listbox.delete(0, "end")

        for index, question in enumerate(self.all_questions):
            self.questions_listbox.insert("end", f"{index + 1}. {question[2]}")

    def _on_test_selected(self, event):
        selection = self.tests_listbox.curselection()
        if not selection:
            return

        self.current_test_id = self.all_tests[selection[0]][0]
        self._load_questions()
        self._clear_editor()

    def _on_question_selected(self, event):
        selection = self.questions_listbox.curselection()
        if not selection:
            return

        # Структура рядка: (id, test_id, question, a1, a2, a3, a4, correct_answer)
        question = self.all_questions[selection[0]]

        self.question_entry.delete(0, "end")
        self.question_entry.insert(0, question[2])

        for i, entry in enumerate(self.answer_entries):
            entry.delete(0, "end")
            entry.insert(0, question[3 + i])

        correct_indices = question[7].split(",") if question[7] else []
        for i, var in enumerate(self.correct_vars):
            var.set(1 if str(i) in correct_indices else 0)

    def _save_question_changes(self):
        selection = self.questions_listbox.curselection()
        if not selection:
            messagebox.showerror("Помилка", "Оберіть питання для редагування.")
            return

        question_text = self.question_entry.get().strip()
        answers       = [e.get().strip() for e in self.answer_entries]
        correct       = [i for i, v in enumerate(self.correct_vars) if v.get() == 1]

        if not question_text or any(not a for a in answers):
            messagebox.showerror("Помилка", "Заповніть усі поля.")
            return

        question_id = self.all_questions[selection[0]][0]
        correct_str = ",".join(map(str, correct))

        try:
            self.test_manager.update_question(
                question_id,
                question_text,
                answers[0], answers[1], answers[2], answers[3],
                correct_str
            )
            self._load_questions()
            messagebox.showinfo("Готово", "Питання оновлено!")
        except Exception as error:
            messagebox.showerror("Помилка БД", str(error))

    def _delete_selected_question(self):
        selection = self.questions_listbox.curselection()
        if not selection:
            return

        question_id = self.all_questions[selection[0]][0]

        try:
            self.test_manager.delete_question(question_id)
            self._load_questions()
            self._clear_editor()
        except Exception as error:
            messagebox.showerror("Помилка БД", str(error))

    def _delete_selected_test(self):
        selection = self.tests_listbox.curselection()
        if not selection:
            messagebox.showerror("Помилка", "Оберіть тест для видалення.")
            return

        test_id, test_name = self.all_tests[selection[0]]

        confirmed = messagebox.askyesno("Підтвердження", f"Видалити тест '{test_name}'?")
        if not confirmed:
            return

        try:
            self.test_manager.delete_test(test_id)
            self.current_test_id = None
            self.all_questions   = []
            self._load_tests()
            self.questions_listbox.delete(0, "end")
            self._clear_editor()
        except Exception as error:
            messagebox.showerror("Помилка БД", str(error))

    def _clear_editor(self):
        """Очищує всі поля редактора питання."""
        self.question_entry.delete(0, "end")
        for entry in self.answer_entries:
            entry.delete(0, "end")
        for var in self.correct_vars:
            var.set(0)
