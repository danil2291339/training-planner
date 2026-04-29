import json
import os
from tkinter import *
from tkinter import messagebox, ttk
from datetime import datetime

DATA_FILE = "trainings.json"

# Загрузка данных
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

# Сохранение данных
def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

class TrainingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Training Planner - План тренировок")
        self.root.geometry("850x550")
        self.data = load_data()

        # ========== Поля ввода ==========
        input_frame = LabelFrame(root, text="Добавить тренировку", padx=10, pady=10)
        input_frame.pack(fill=X, padx=10, pady=5)

        Label(input_frame, text="Дата (ГГГГ-ММ-ДД):").grid(row=0, column=0, padx=5, pady=5)
        self.date_entry = Entry(input_frame, width=12)
        self.date_entry.grid(row=0, column=1, padx=5, pady=5)
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))

        Label(input_frame, text="Тип тренировки:").grid(row=0, column=2, padx=5, pady=5)
        self.type_var = StringVar(value="бег")
        self.type_menu = ttk.Combobox(input_frame, textvariable=self.type_var,
                                      values=["бег", "велосипед", "плавание", "силовая", "йога", "стретчинг"],
                                      width=12, state="readonly")
        self.type_menu.grid(row=0, column=3, padx=5, pady=5)

        Label(input_frame, text="Длительность (мин):").grid(row=0, column=4, padx=5, pady=5)
        self.duration_entry = Entry(input_frame, width=10)
        self.duration_entry.grid(row=0, column=5, padx=5, pady=5)

        Button(input_frame, text="➕ Добавить тренировку", command=self.add_training, bg="lightgreen").grid(row=0, column=6, padx=10, pady=5)

        # ========== Фильтры ==========
        filter_frame = LabelFrame(root, text="Фильтрация", padx=10, pady=10)
        filter_frame.pack(fill=X, padx=10, pady=5)

        Label(filter_frame, text="Тип тренировки:").grid(row=0, column=0, padx=5, pady=5)
        self.filter_type = StringVar(value="все")
        ttk.Combobox(filter_frame, textvariable=self.filter_type,
                     values=["все", "бег", "велосипед", "плавание", "силовая", "йога", "стретчинг"],
                     width=12, state="readonly").grid(row=0, column=1, padx=5, pady=5)

        Label(filter_frame, text="Дата от (ГГГГ-ММ-ДД):").grid(row=0, column=2, padx=5, pady=5)
        self.date_from = Entry(filter_frame, width=12)
        self.date_from.grid(row=0, column=3, padx=5, pady=5)

        Label(filter_frame, text="Дата до (ГГГГ-ММ-ДД):").grid(row=0, column=4, padx=5, pady=5)
        self.date_to = Entry(filter_frame, width=12)
        self.date_to.grid(row=0, column=5, padx=5, pady=5)

        Button(filter_frame, text="🔍 Применить фильтр", command=self.apply_filter, bg="lightyellow").grid(row=0, column=6, padx=10, pady=5)
        Button(filter_frame, text="🔄 Сбросить фильтр", command=self.reset_filter, bg="lightgray").grid(row=0, column=7, padx=5, pady=5)

        # ========== Таблица с тренировками ==========
        table_frame = Frame(root)
        table_frame.pack(fill=BOTH, expand=True, padx=10, pady=5)

        self.tree = ttk.Treeview(table_frame, columns=("ID", "Дата", "Тип", "Длительность"), show="headings", height=15)
        self.tree.heading("ID", text="№")
        self.tree.heading("Дата", text="Дата")
        self.tree.heading("Тип", text="Тип тренировки")
        self.tree.heading("Длительность", text="Длительность (мин)")

        self.tree.column("ID", width=40)
        self.tree.column("Дата", width=100)
        self.tree.column("Тип", width=120)
        self.tree.column("Длительность", width=100)

        scrollbar = Scrollbar(table_frame, orient=VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=RIGHT, fill=Y)
        self.tree.pack(fill=BOTH, expand=True)

        # Кнопка удаления
        Button(root, text="🗑 Удалить выбранную запись", command=self.delete_training, bg="lightcoral").pack(pady=5)

        self.display_data(self.data)

    def add_training(self):
        date = self.date_entry.get().strip()
        training_type = self.type_var.get()
        duration = self.duration_entry.get().strip()

        # Валидация даты
        if not date:
            messagebox.showerror("Ошибка", "Введите дату!")
            return
        try:
            datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Ошибка", "Неверный формат даты! Используйте ГГГГ-ММ-ДД")
            return

        # Валидация длительности
        if not duration:
            messagebox.showerror("Ошибка", "Введите длительность!")
            return
        try:
            duration = float(duration)
            if duration <= 0:
                messagebox.showerror("Ошибка", "Длительность должна быть положительным числом!")
                return
        except ValueError:
            messagebox.showerror("Ошибка", "Длительность должна быть числом!")
            return

        training = {
            "id": len(self.data) + 1,
            "date": date,
            "type": training_type,
            "duration": duration
        }
        self.data.append(training)
        save_data(self.data)
        self.display_data(self.data)
        self.duration_entry.delete(0, END)
        messagebox.showinfo("Успех", f"Тренировка добавлена!")

    def display_data(self, records):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for r in records:
            self.tree.insert("", END, values=(r["id"], r["date"], r["type"], r["duration"]))

    def apply_filter(self):
        filtered = self.data.copy()
        training_type = self.filter_type.get()
        date_from = self.date_from.get().strip()
        date_to = self.date_to.get().strip()

        if training_type != "все":
            filtered = [t for t in filtered if t["type"] == training_type]

        if date_from:
            try:
                datetime.strptime(date_from, "%Y-%m-%d")
                filtered = [t for t in filtered if t["date"] >= date_from]
            except ValueError:
                messagebox.showerror("Ошибка", "Неверный формат даты 'от'!")
                return

        if date_to:
            try:
                datetime.strptime(date_to, "%Y-%m-%d")
                filtered = [t for t in filtered if t["date"] <= date_to]
            except ValueError:
                messagebox.showerror("Ошибка", "Неверный формат даты 'до'!")
                return

        self.display_data(filtered)

    def reset_filter(self):
        self.filter_type.set("все")
        self.date_from.delete(0, END)
        self.date_to.delete(0, END)
        self.display_data(self.data)

    def delete_training(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Ошибка", "Выберите запись для удаления!")
            return

        item = selected[0]
        values = self.tree.item(item)["values"]
        training_id = values[0]

        self.data = [t for t in self.data if t["id"] != training_id]
        for i, t in enumerate(self.data):
            t["id"] = i + 1

        save_data(self.data)
        self.apply_filter()
        messagebox.showinfo("Успех", "Запись удалена!")

# Запуск
if __name__ == "__main__":
    root = Tk()
    app = TrainingApp(root)
    root.mainloop()