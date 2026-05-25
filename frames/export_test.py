import json
import ttkbootstrap as ttk
from tkinter import filedialog, messagebox
import tkfontawesome as fa

from .base_frame import SelectionScreen
from config import STYLE


class ExportTestSelection(SelectionScreen):

    def __init__(self, parent, controller):
        super().__init__(
            parent, controller,
            title_text="Оберіть тест для експорту:",
            back_frame="AdminMenu"
        )
        self.icon_export = fa.icon_to_image(
            "file-export", fill=STYLE["colors"]["accent"], scale_to_height=20
        )

    def on_show(self, **kwargs):
        for widget in self.buttons_frame.winfo_children():
            widget.destroy()

        all_tests = self.test_manager.get_tests()

        if not all_tests:
            ttk.Label(
                self.buttons_frame,
                text="Немає доступних тестів!",
                font=STYLE["fonts"]["button"],
                bootstyle="danger"
            ).pack(pady=10)
        else:
            for test_id, test_name in all_tests:
                ttk.Button(
                    self.buttons_frame,
                    text=f"  {test_name}",
                    image=self.icon_export,
                    compound="left",
                    bootstyle="primary-outline",
                    command=lambda tid=test_id, name=test_name: self.export_test(tid, name)
                ).pack(pady=5, fill="x", ipady=5)

    def export_test(self, test_id, test_name):
        file_path = filedialog.asksaveasfilename(
            title="Зберегти тест як...",
            initialfile=f"{test_name}.json",
            defaultextension=".json",
            filetypes=[("JSON файли", "*.json")]
        )
        if not file_path:
            return  # Користувач закрив діалог

        try:
            questions = self.test_manager.get_questions(test_id)

            questions_data = [
                {
                    "question":       q[2],
                    "answer1":        q[3],
                    "answer2":        q[4],
                    "answer3":        q[5],
                    "answer4":        q[6],
                    "correct_answer": q[7],
                }
                for q in questions
            ]

            export_data = {
                "test_name": test_name,
                "questions": questions_data,
            }

            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(export_data, f, ensure_ascii=False, indent=4)

            messagebox.showinfo("Успіх", f"Тест '{test_name}' успішно збережено!")

        except Exception as error:
            messagebox.showerror("Помилка експорту", f"Не вдалося зберегти файл.\n{error}")
