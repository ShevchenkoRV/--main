import ttkbootstrap as ttk
from tkinter import messagebox, Canvas
import tkfontawesome as fa

from .base_frame import BaseFrame
from config import STYLE


class StudentMenu(BaseFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        self.selected_test = ttk.StringVar()
        self.student_name  = ttk.StringVar()

        self.icon_start = fa.icon_to_image("play-circle", fill="white", scale_to_height=20)
        self.icon_back  = fa.icon_to_image("arrow-left",  fill="white", scale_to_height=20)

        self._build_ui()

        # Відстежуємо зміни в полі імені, щоб оновлювати стан кнопки "Почати"
        self.student_name.trace_add("write", self._validate_form)

    def _build_ui(self):
        container = ttk.Frame(self)
        container.pack(expand=True, fill="both", padx=100, pady=20)

        # Крок 1 — список тестів з прокруткою
        ttk.Label(container, text="1. Оберіть тест:", font=STYLE["fonts"]["header"]).pack(anchor="w")

        list_container = ttk.Frame(container)
        list_container.pack(pady=10, fill="both", expand=True)
        list_container.rowconfigure(0, weight=1)
        list_container.columnconfigure(0, weight=1)

        canvas = Canvas(list_container, highlightthickness=0)
        scrollbar = ttk.Scrollbar(list_container, orient="vertical",
                                  command=canvas.yview, bootstyle="round")
        canvas.configure(yscrollcommand=scrollbar.set)

        self.tests_frame = ttk.Frame(canvas)
        canvas.create_window((0, 0), window=self.tests_frame, anchor="nw")
        self.tests_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        ttk.Separator(container, orient="horizontal").pack(fill="x", pady=20)

        # Крок 2 — поле для імені
        ttk.Label(container, text="2. Введіть ваше ПІБ:", font=STYLE["fonts"]["header"]).pack(anchor="w", pady=(10, 5))

        ttk.Entry(container, textvariable=self.student_name,
                  font=STYLE["fonts"]["entry"], width=50
                  ).pack(pady=5, ipady=5, anchor="w")

        # Кнопка "Почати"
        self.start_button = ttk.Button(
            container,
            text=" Почати тестування",
            width=25,
            image=self.icon_start,
            compound="left",
            bootstyle="success",
            state="disabled",
            command=self._start_test
        )
        self.start_button.pack(pady=20, anchor="w", ipady=5)

        # Кнопка "Назад"
        ttk.Button(
            self,
            text=" Назад",
            image=self.icon_back,
            compound="left",
            bootstyle="secondary",
            command=lambda: self.controller.show_frame("MainMenu")
        ).pack(pady=20)

    def on_show(self, **kwargs):

        self.selected_test.set("")
        self.student_name.set("")

        for widget in self.tests_frame.winfo_children():
            widget.destroy()

        all_tests = self.test_manager.get_tests()

        if not all_tests:
            ttk.Label(
                self.tests_frame,
                text="Немає доступних тестів!",
                font=STYLE["fonts"]["button"],
                bootstyle="danger"
            ).pack(pady=10)
        else:
            for _, test_name in all_tests:
                ttk.Radiobutton(
                    self.tests_frame,
                    text=test_name,
                    variable=self.selected_test,
                    value=test_name,
                    bootstyle="primary",
                    command=self._validate_form
                ).pack(pady=5, fill="x", padx=10)


    def _validate_form(self, *args):
        test_chosen = bool(self.selected_test.get())
        name_filled = bool(self.student_name.get().strip())

        state = "normal" if test_chosen and name_filled else "disabled"
        self.start_button.config(state=state)

    def _start_test(self):
        test_name    = self.selected_test.get()
        student_name = self.student_name.get().strip()

        if not test_name or not student_name:
            messagebox.showwarning("Увага", "Оберіть тест та введіть ваше ім'я.")
            return

        self.controller.show_frame("TestTaking", test_name=test_name, student_name=student_name)
