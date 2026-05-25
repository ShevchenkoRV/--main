
import ttkbootstrap as ttk
from config import STYLE


class BaseFrame(ttk.Frame):
    """Базовий екран. Всі інші екрани наслідуються від нього."""

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller   = controller
        self.test_manager = controller.test_manager


class SelectionScreen(BaseFrame):


    def __init__(self, parent, controller, title_text, back_frame):
        super().__init__(parent, controller)

        container = ttk.Frame(self)
        container.pack(expand=True)

        # Заголовок
        self.title_label = ttk.Label(
            container,
            text=title_text,
            font=STYLE["fonts"]["title"]
        )
        self.title_label.pack(pady=40)

        # Сюди підкласи додають свої кнопки
        self.buttons_frame = ttk.Frame(container)
        self.buttons_frame.pack(pady=10, fill="x", padx=100)

        # Кнопка "Назад"
        ttk.Button(
            container,
            text="Назад",
            width=25,
            bootstyle="secondary",
            command=lambda: controller.show_frame(back_frame)
        ).pack(pady=40)
