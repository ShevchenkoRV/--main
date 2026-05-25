
import ttkbootstrap as ttk
from tkinter import simpledialog, messagebox

import database  # імпорт ініціалізує таблиці в БД
from test_manager import TestManager
from config import STYLE, ADMIN_PASSWORD

from frames import (
    MainMenu,
    AdminMenu,
    TestConstructor,
    EditTest,
    StudentStatisticsSelection,
    StudentStatisticsViewer,
    ExportTestSelection,
    StudentMenu,
    TestTaking,
    ResultsScreen,
)

# Список усіх екранів програми
ALL_SCREENS = (
    MainMenu,
    AdminMenu,
    TestConstructor,
    EditTest,
    StudentStatisticsSelection,
    StudentStatisticsViewer,
    ExportTestSelection,
    StudentMenu,
    TestTaking,
    ResultsScreen,
)


class TestingApp(ttk.Window):


    def __init__(self):
        super().__init__(themename="flatly")

        self.title("Система тестування")
        self.geometry("1024x768")
        self.attributes("-fullscreen", True)
        self.bind("<Escape>", lambda e: self.attributes("-fullscreen", False))

        self._setup_styles()
        self.test_manager = TestManager()

        # Контейнер, у якому всі екрани лежать один поверх одного
        container = ttk.Frame(self)
        container.pack(fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Створюємо та реєструємо всі екрани
        self.screens = {}
        for ScreenClass in ALL_SCREENS:
            name = ScreenClass.__name__
            screen = ScreenClass(parent=container, controller=self)
            self.screens[name] = screen
            screen.grid(row=0, column=0, sticky="nsew")

        self.show_frame("MainMenu")

    def _setup_styles(self):

        style = ttk.Style()
        style.configure("TCheckbutton",          font=STYLE["fonts"]["button"])
        style.configure("TRadiobutton",           font=STYLE["fonts"]["button"])
        style.configure("LargeToggle.TCheckbutton", padding=[0, 10, 0, 10])

    def show_frame(self, screen_name, **kwargs):

        screen = self.screens[screen_name]

        if hasattr(screen, "on_show"):
            screen.on_show(**kwargs)

        screen.tkraise()

    def prompt_admin_password(self):
        password = simpledialog.askstring(
            "Вхід адміністратора",
            "Введіть пароль:",
            show="*"
        )

        if password == ADMIN_PASSWORD:
            self.show_frame("AdminMenu")
        elif password is not None:
            # Користувач щось ввів, але пароль неправильний
            messagebox.showerror("Помилка", "Неправильний пароль!")


if __name__ == "__main__":
    app = TestingApp()
    app.mainloop()
