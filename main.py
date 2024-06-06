import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3

# Инициализация базы данных
def init_db():
    conn = sqlite3.connect('business_orders.db')
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY,
    customer_name TEXT NOT NULL,
    product_sku TEXT NOT NULL,
    product_name TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    order_date TEXT NOT NULL,
    status TEXT NOT NULL)
    """)
    conn.commit()
    conn.close()

# Добавление нового заказа
def add_order():
    conn = sqlite3.connect('business_orders.db')
    cur = conn.cursor()
    cur.execute("INSERT INTO orders (customer_name, product_sku, product_name, quantity, order_date, status) VALUES (?, ?, ?, ?, ?, ?)",
                (customer_name_entry.get(), product_sku_entry.get(), product_name_entry.get(), quantity_entry.get(), order_date_entry.get(), 'Новый заказ'))
    conn.commit()
    conn.close()
    customer_name_entry.delete(0, tk.END)
    product_sku_entry.delete(0, tk.END)
    product_name_entry.delete(0, tk.END)
    quantity_entry.delete(0, tk.END)
    order_date_entry.delete(0, tk.END)
    view_orders()

# Просмотр всех заказов
def view_orders():
    for i in tree.get_children():
        tree.delete(i)
    conn = sqlite3.connect('business_orders.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM orders")
    rows = cur.fetchall()
    for row in rows:
        tree.insert("", tk.END, values=row)
    conn.close()

# Завершение заказа
def complete_order():
    selected_item = tree.selection()
    if selected_item:
        order_id = tree.item(selected_item, 'values')[0]
        conn = sqlite3.connect('business_orders.db')
        cur = conn.cursor()
        cur.execute("UPDATE orders SET status='Завершён' WHERE id=?", (order_id,))
        conn.commit()
        conn.close()
        view_orders()
    else:
        messagebox.showwarning("Предупреждение", "Выберите заказ для завершения")

# Анализ заказов (пример)
def analyze_orders():
    # Здесь можно добавить логику анализа заказов
    messagebox.showinfo("Анализ заказов", "Функция анализа заказов пока не реализована")

# Инициализация базы данных
init_db()

# Создание окна приложения
app = tk.Tk()
app.title("Система управления заказами")

# Поля ввода
tk.Label(app, text="Имя клиента").pack()
customer_name_entry = tk.Entry(app)
customer_name_entry.pack()

tk.Label(app, text="Артикул товара").pack()
product_sku_entry = tk.Entry(app)
product_sku_entry.pack()

tk.Label(app, text="Наименование товара").pack()
product_name_entry = tk.Entry(app)
product_name_entry.pack()

tk.Label(app, text="Количество единиц товара").pack()
quantity_entry = tk.Entry(app)
quantity_entry.pack()

tk.Label(app, text="Дата заказа").pack()
order_date_entry = tk.Entry(app)
order_date_entry.pack()

# Кнопка для добавления заказа
add_button = tk.Button(app, text="Добавить заказ", command=add_order)
add_button.pack()

# Кнопка для завершения заказа
complete_button = tk.Button(app, text="Завершить заказ", command=complete_order)
complete_button.pack()

# Кнопка для анализа заказов
analyze_button = tk.Button(app, text="Анализ заказов", command=analyze_orders)
analyze_button.pack()

# Таблица для отображения заказов
columns = ("id", "customer_name", "product_sku", "product_name", "quantity", "order_date", "status")
tree = ttk.Treeview(app, columns=columns, show="headings")
for column in columns:
    tree.heading(column, text=column)
tree.pack()

# Отображение всех заказов
view_orders()

# Запуск основного цикла приложения
app.mainloop()
