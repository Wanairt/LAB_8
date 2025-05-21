import tkinter as tk
from tkinter import messagebox
from collections import defaultdict
import csv

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


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
        self.products = Product.load_from_file()

        if not self.products:
            messagebox.showerror("Ошибка", "Нет данных для анализа.")
            return

        tk.Button(root, text="По категориям", command=self.show_by_category).pack(pady=5)
        tk.Button(root, text="По продажам", command=self.show_by_sales).pack(pady=5)

        self.canvas_frame = tk.Frame(root)
        self.canvas_frame.pack()

    def draw_pie(self, data, title):
        for widget in self.canvas_frame.winfo_children():
            widget.destroy()

        fig = Figure(figsize=(5, 4))
        ax = fig.add_subplot(111)
        ax.pie(data.values(), labels=data.keys(), autopct='%1.1f%%')
        ax.set_title(title)

        chart = FigureCanvasTkAgg(fig, self.canvas_frame)
        chart.draw()
        chart.get_tk_widget().pack()

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
