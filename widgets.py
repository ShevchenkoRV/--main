
import tkinter as tk
from config import STYLE

class StyledButton(tk.Button):

    def __init__(self, master, bg_color=STYLE["colors"]["accent"], hover_color=None, **kwargs):
        super().__init__(master, **kwargs)
        self.bg_color = bg_color
        self.hover_color = hover_color or (STYLE["colors"]["accent_hover"] if bg_color == STYLE["colors"]["accent"] else "#D32F2F")

        self.config(
            font=STYLE["fonts"]["button"],
            bg=self.bg_color,
            fg="white",
            relief="flat",
            borderwidth=0,
            padx=STYLE["padding"]["medium"],
            pady=STYLE["padding"]["small"],
            activebackground=self.hover_color,
            activeforeground="white"
        )
        self.bind("<Enter>", lambda e: self.config(bg=self.hover_color))
        self.bind("<Leave>", lambda e: self.config(bg=self.bg_color))