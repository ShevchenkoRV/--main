import ttkbootstrap as ttk
import tkfontawesome as fa

from .base_frame import BaseFrame
from config import STYLE


class MainMenu(BaseFrame):

    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        # Іконки завантажуємо один раз при ініціалізації
        self.admin_icon   = fa.icon_to_image("user-shield",    fill="white", scale_to_height=20)
        self.student_icon = fa.icon_to_image("user-graduate",  fill="white", scale_to_height=20)
        self.exit_icon    = fa.icon_to_image("sign-out-alt",   fill="white", scale_to_height=20)

        container = ttk.Frame(self)
        container.pack(expand=True)

        ttk.Label(
            container,
            text="Оберіть режим:",
            font=STYLE["fonts"]["title"]
        ).pack(pady=STYLE["padding"]["large"])

        ttk.Button(
            container,
            text=" Адміністратор",
            width=25,
            image=self.admin_icon,
            compound="left",
            bootstyle="primary",
            command=controller.prompt_admin_password
        ).pack(pady=STYLE["padding"]["medium"], ipady=5)

        ttk.Button(
            container,
            text=" Студент",
            width=25,
            image=self.student_icon,
            compound="left",
            bootstyle="primary",
            command=lambda: controller.show_frame("StudentMenu")
        ).pack(pady=STYLE["padding"]["medium"], ipady=5)

        ttk.Button(
            container,
            text=" Вихід",
            width=25,
            image=self.exit_icon,
            compound="left",
            bootstyle="danger",
            command=self.quit
        ).pack(pady=(STYLE["padding"]["large"], 0), ipady=5)
