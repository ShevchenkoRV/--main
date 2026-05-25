import ttkbootstrap as ttk
from tkinter import messagebox, Listbox
import tkfontawesome as fa

from .base_frame import BaseFrame
from config import STYLE


class TestConstructor(BaseFrame):

    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        # Список питань, що додаються до тесту (ще не збережені в БД)
        self.pending_questions = []

        self._build_ui()

    def _build_ui(self):
        # Поле для назви тесту
        name_section = ttk.Frame(self)
        name_section.pack(fill="x", padx=20, pady=10)

        ttk.Label(name_section, text="Назва тесту:", font=STYLE["fonts"]["default"]).pack(anchor="w")
        self.test_name_entry = ttk.Entry(name_section, font=STYLE["fonts"]["entry"])
        self.test_name_entry.pack(fill="x", pady=5)

        # Основна область — ліво: список, право: форма питання
        main_area = ttk.Frame(self)
        main_area.pack(fill="both", expand=True, padx=20, pady=10)

        self._build_question_list(main_area)
        self._build_question_form(main_area)

        # Кнопки "Зберегти" і "Назад"
        bottom = ttk.Frame(self)
        bottom.pack(side="bottom", pady=10)

        ttk.Button(bottom, text="Зберегти тест", bootstyle="success",
                   command=self._save_test).pack(side="left", padx=5)
        ttk.Button(bottom, text="Назад", bootstyle="secondary",
                   command=lambda: self.controller.show_frame("AdminMenu")).pack(side="left", padx=5)

    def _build_question_list(self, parent):
        column = ttk.Frame(parent)
        column.pack(side="left", fill="both", expand=True)

        ttk.Label(column, text="Питання:", font=STYLE["fonts"]["default"]).pack(anchor="w")

        self.questions_listbox = Listbox(column, height=15)
        self.questions_listbox.pack(fill="both", expand=True)

    def _build_question_form(self, parent):

        column = ttk.Frame(parent)
        column.pack(side="right", fill="both", expand=True)

        ttk.Label(column, text="Текст питання:", font=STYLE["fonts"]["default"]).pack(anchor="w")

        self.question_text_entry = ttk.Entry(column)
        self.question_text_entry.pack(fill="x", pady=5)

        # Чотири варіанти відповіді з позначкою "правильна"
        self.answer_entries = []
        self.correct_vars   = []

        for i in range(4):
            row = ttk.Frame(column)
            row.pack(fill="x", pady=2)

            var = ttk.IntVar()
            ttk.Checkbutton(row, variable=var).pack(side="left")

            entry = ttk.Entry(row)
            entry.pack(side="left", fill="x", expand=True)

            self.correct_vars.append(var)
            self.answer_entries.append(entry)

        # Кнопки "Додати" і "Видалити"
        actions = ttk.Frame(column)
        actions.pack(fill="x", pady=10)

        ttk.Button(actions, text="Додати питання",
                   command=self._add_question).pack(fill="x", pady=2)
        ttk.Button(actions, text="Видалити обране", bootstyle="danger",
                   command=self._delete_selected_question).pack(fill="x", pady=2)

    def on_show(self, **kwargs):
        """Скидає форму до початкового стану."""
        self.pending_questions = []
        self.test_name_entry.delete(0, "end")
        self._refresh_list()
        self._clear_form()


    def _add_question(self):
        """Додає питання до тимчасового списку (без запису в БД)."""
        question_text = self.question_text_entry.get().strip()
        answers       = [e.get().strip() for e in self.answer_entries]
        correct       = [i for i, v in enumerate(self.correct_vars) if v.get() == 1]

        if not question_text or any(not a for a in answers):
            messagebox.showerror("Помилка", "Заповніть усі поля питання.")
            return

        self.pending_questions.append({
            "question": question_text,
            "answers":  answers,
            "correct":  correct,
        })

        self._refresh_list()
        self._clear_form()

    def _delete_selected_question(self):

        selection = self.questions_listbox.curselection()
        if not selection:
            return

        del self.pending_questions[selection[0]]
        self._refresh_list()

    def _save_test(self):
        test_name = self.test_name_entry.get().strip()

        if not test_name:
            messagebox.showerror("Помилка", "Введіть назву тесту.")
            return

        if not self.pending_questions:
            messagebox.showerror("Помилка", "Додайте хоча б одне питання.")
            return

        try:
            test_id = self.test_manager.add_test(test_name)

            for q in self.pending_questions:
                self.test_manager.add_question(
                    test_id,
                    q["question"],
                    q["answers"][0],
                    q["answers"][1],
                    q["answers"][2],
                    q["answers"][3],
                    ",".join(map(str, q["correct"]))
                )

            messagebox.showinfo("Готово", f"Тест '{test_name}' створено!")
            self.controller.show_frame("AdminMenu")

        except Exception as error:
            messagebox.showerror("Помилка БД", str(error))

    def _refresh_list(self):
        self.questions_listbox.delete(0, "end")
        for i, q in enumerate(self.pending_questions):
            self.questions_listbox.insert("end", f"{i + 1}. {q['question']}")

    def _clear_form(self):
        self.question_text_entry.delete(0, "end")
        for entry in self.answer_entries:
            entry.delete(0, "end")
        for var in self.correct_vars:
            var.set(0)
