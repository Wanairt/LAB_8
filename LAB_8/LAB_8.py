import tkinter as tk
from tkinter import messagebox
from collections import defaultdict
import csv


class Product:
    def __init__(self, name, category, sales):
        self.name = name
        self.category = category
        self.sales = sales

    @staticmethod
    def load_from_file(filename="products.csv"):
        products = []
        try:
            with open(filename, encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    try:
                        sales = int(row['sales'])
                        product = Product(row['name'], row['category'], sales)
                        products.append(product)
                    except ValueError:
                        print(f"Ошибка в строке: {row}")
        except FileNotFoundError:
            messagebox.showerror("Ошибка", f"Файл {filename} не найден.")
        return products

    @staticmethod
    def segment_by_category(products):
        counts = defaultdict(int)
        for p in products:
            counts[p.category] += 1
        return counts

    @staticmethod
    def segment_by_sales(products):
        sales = defaultdict(int)
        for p in products:
            sales[p.category] += p.sales
        return sales


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Анализ товаров")
        self.root.geometry("800x600")
        self.root.resizable(False, False)

        self.products = Product.load_from_file()
        if not self.products:
            messagebox.showerror("Ошибка", "Нет данных для анализа.")
            return

        # --- Рамка для кнопок ---
        button_frame = tk.Frame(root)
        button_frame.pack(pady=20, fill="x")

        btn_style = {
            "font": ("Arial", 14, "bold"),
            "width": 20,
            "height": 2,
            "relief": "raised",
            "bd": 2
        }

        tk.Button(
            button_frame, text="По категориям",
            command=self.show_by_category, **btn_style
        ).pack(side="left", expand=True, padx=20)

        tk.Button(
            button_frame, text="По продажам",
            command=self.show_by_sales, **btn_style
        ).pack(side="left", expand=True, padx=20)

        # --- Рамка для графиков ---
        self.canvas_frame = tk.Frame(root)
        self.canvas_frame.pack(expand=True, fill="both", padx=10, pady=10)

        self.canvas = tk.Canvas(self.canvas_frame, bg="white")
        self.canvas.pack(expand=True, fill="both")

    def draw_pie(self, data, title):
        self.canvas.delete("all")

        total = sum(data.values())
        if total == 0:
            self.canvas.create_text(400, 300, text="Нет данных", font=("Arial", 16))
            return

        x0, y0, x1, y1 = 250, 170, 550, 470

        start_angle = 0
        colors = ["#FF9999", "#99FF99", "#9999FF", "#FFCC99", "#FFFF99", "#CC99FF"]

        for i, (key, value) in enumerate(data.items()):
            extent = (value / total) * 360
            color = colors[i % len(colors)]
            self.canvas.create_arc(x0, y0, x1, y1, start=start_angle,
                                   extent=extent, fill=color, outline="black")
            start_angle += extent

        self.canvas.create_text(400, 60, text=title, font=("Arial", 20, "bold"))

        legend_x, legend_y = 600, 150
        for i, (key, value) in enumerate(data.items()):
            percent = (value / total) * 100
            color = colors[i % len(colors)]
            self.canvas.create_rectangle(legend_x, legend_y + i * 30,
                                         legend_x + 20, legend_y + i * 30 + 20,
                                         fill=color, outline="black")
            self.canvas.create_text(legend_x + 30, legend_y + i * 30 + 10,
                                    text=f"{key}: {percent:.1f}%",
                                    anchor="w", font=("Arial", 12))

    def show_by_category(self):
        data = Product.segment_by_category(self.products)
        self.draw_pie(data, "Товары по категориям")

    def show_by_sales(self):
        data = Product.segment_by_sales(self.products)
        self.draw_pie(data, "Продажи по категориям")


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()