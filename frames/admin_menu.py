import json
import ttkbootstrap as ttk
from tkinter import filedialog, messagebox
import tkfontawesome as fa

from .base_frame import BaseFrame
from config import STYLE


class AdminMenu(BaseFrame):

    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        # Іконки для кнопок
        self.icon_create = fa.icon_to_image("plus-circle",  fill="white", scale_to_height=30)
        self.icon_edit   = fa.icon_to_image("pencil-alt",   fill="white", scale_to_height=30)
        self.icon_stats  = fa.icon_to_image("chart-bar",    fill="white", scale_to_height=30)
        self.icon_import = fa.icon_to_image("file-import",  fill="white", scale_to_height=30)
        self.icon_export = fa.icon_to_image("file-export",  fill="white", scale_to_height=30)
        self.icon_back   = fa.icon_to_image("arrow-left",   fill="white", scale_to_height=20)

        container = ttk.Frame(self)
        container.pack(expand=True, fill="both", padx=50, pady=20)
        container.columnconfigure((0, 1, 2), weight=1)

        ttk.Label(
            container,
            text="Панель адміністратора",
            font=STYLE["fonts"]["title"]
        ).grid(row=0, column=0, columnspan=3, pady=STYLE["padding"]["large"])

        # --- Перший ряд кнопок ---
        ttk.Button(
            container,
            text="Створити тест",
            image=self.icon_create,
            compound="top",
            bootstyle="success",
            command=lambda: controller.show_frame("TestConstructor")
        ).grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

        ttk.Button(
            container,
            text="Редагувати тест",
            image=self.icon_edit,
            compound="top",
            bootstyle="primary",
            command=lambda: controller.show_frame("EditTest")
        ).grid(row=1, column=1, sticky="nsew", padx=10, pady=10)

        ttk.Button(
            container,
            text="Статистика",
            image=self.icon_stats,
            compound="top",
            bootstyle="info",
            command=lambda: controller.show_frame("StudentStatisticsSelection")
        ).grid(row=1, column=2, sticky="nsew", padx=10, pady=10)

        # --- Другий ряд кнопок ---
        ttk.Button(
            container,
            text="Імпорт тесту",
            image=self.icon_import,
            compound="top",
            bootstyle="warning",
            command=self.import_test
        ).grid(row=2, column=0, sticky="nsew", padx=10, pady=10)

        ttk.Button(
            container,
            text="Експорт тесту",
            image=self.icon_export,
            compound="top",
            bootstyle="warning",
            command=lambda: controller.show_frame("ExportTestSelection")
        ).grid(row=2, column=1, sticky="nsew", padx=10, pady=10)

        # --- Кнопка "Назад" внизу ---
        ttk.Button(
            self,
            text=" Назад",
            image=self.icon_back,
            compound="left",
            bootstyle="secondary",
            command=lambda: controller.show_frame("MainMenu")
        ).pack(side="bottom", pady=20, padx=50, anchor="w")

    def import_test(self):
        """Імпортує тест з JSON-файлу у базу даних."""
        file_path = filedialog.askopenfilename(
            title="Оберіть файл для імпорту",
            filetypes=[("JSON файли", "*.json")]
        )
        if not file_path:
            return  # Користувач закрив діалог

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            # Перевіряємо структуру файлу
            if not isinstance(data, dict) or "test_name" not in data or "questions" not in data:
                raise ValueError("Неправильний формат файлу.")

            test_name = data["test_name"]
            questions = data["questions"]

            # Якщо тест з таким іменем вже існує — запитуємо про перезапис
            existing_tests = self.test_manager.get_tests()
            existing_names = {name: tid for tid, name in existing_tests}

            if test_name in existing_names:
                overwrite = messagebox.askyesno(
                    "Увага",
                    f"Тест '{test_name}' вже існує. Перезаписати?"
                )
                if not overwrite:
                    return
                self.test_manager.delete_test(existing_names[test_name])

            # Зберігаємо тест і всі його питання
            test_id = self.test_manager.add_test(test_name)
            for q in questions:
                self.test_manager.add_question(
                    test_id,
                    q["question"],
                    q["answer1"],
                    q["answer2"],
                    q["answer3"],
                    q["answer4"],
                    q["correct_answer"]
                )

            messagebox.showinfo("Успіх", f"Тест '{test_name}' успішно імпортовано!")

        except Exception as error:
            messagebox.showerror("Помилка імпорту", f"Не вдалося імпортувати тест.\n{error}")
