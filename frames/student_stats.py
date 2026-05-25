import ttkbootstrap as ttk
import tkfontawesome as fa

from .base_frame import BaseFrame, SelectionScreen
from config import STYLE


class StudentStatisticsSelection(SelectionScreen):

    def __init__(self, parent, controller):
        super().__init__(
            parent, controller,
            title_text="Статистика студентів",
            back_frame="AdminMenu"
        )
        self.icon_student = fa.icon_to_image(
            "user-graduate", fill=STYLE["colors"]["accent"], scale_to_height=20
        )

    def on_show(self, **kwargs):
        for widget in self.buttons_frame.winfo_children():
            widget.destroy()

        students = self.test_manager.get_all_students()

        if not students:
            ttk.Label(
                self.buttons_frame,
                text="Немає збережених результатів.",
                font=STYLE["fonts"]["button"],
                bootstyle="danger"
            ).pack(pady=10)
        else:
            for student_name in students:
                ttk.Button(
                    self.buttons_frame,
                    text=f"  {student_name}",
                    image=self.icon_student,
                    compound="left",
                    bootstyle="primary-outline",
                    command=lambda name=student_name: self.controller.show_frame(
                        "StudentStatisticsViewer", student_name=name
                    )
                ).pack(pady=5, fill="x", ipady=5)


class StudentStatisticsViewer(BaseFrame):

    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        self.icon_back = fa.icon_to_image("arrow-left", fill="white", scale_to_height=20)

        self._build_ui()

    def _build_ui(self):
        self.student_label = ttk.Label(self, text="", font=STYLE["fonts"]["header"])
        self.student_label.pack(pady=20)

        # Таблиця
        table_container = ttk.Frame(self)
        table_container.pack(pady=10, fill="both", expand=True, padx=20)

        columns = ("test_name", "score")
        self.results_table = ttk.Treeview(
            table_container, columns=columns, show="headings", bootstyle="primary"
        )
        self.results_table.heading("test_name", text="Назва тесту")
        self.results_table.heading("score",     text="Результат (балів)")
        self.results_table.column("test_name",  width=500)
        self.results_table.column("score",      width=150, anchor="center")

        scrollbar = ttk.Scrollbar(table_container, orient="vertical",
                                  command=self.results_table.yview, bootstyle="round-primary")
        self.results_table.configure(yscrollcommand=scrollbar.set)
        self.results_table.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.summary_label = ttk.Label(self, text="", font=STYLE["fonts"]["header"])
        self.summary_label.pack(pady=(10, 20))

        ttk.Button(
            self,
            text=" Назад",
            image=self.icon_back,
            compound="left",
            bootstyle="secondary",
            command=lambda: self.controller.show_frame("StudentStatisticsSelection")
        ).pack(pady=20)

    def on_show(self, student_name="", **kwargs):
        self.student_label.config(text=f"Статистика: {student_name}")

        for row in self.results_table.get_children():
            self.results_table.delete(row)

        try:
            results = self.test_manager.get_results_for_student(student_name)
        except Exception as error:
            self.summary_label.config(text=f"Помилка: {error}", bootstyle="danger")
            return

        if not results:
            self.summary_label.config(
                text="Для цього студента немає результатів.",
                bootstyle="danger"
            )
            return

        total_score = 0
        for test_name, score in results:
            self.results_table.insert("", "end", values=(test_name, score))
            total_score += score

        avg_score = total_score / len(results)
        self.summary_label.config(
            text=f"Середній бал: {avg_score:.1f}  |  Всього спроб: {len(results)}",
            bootstyle="success"
        )
