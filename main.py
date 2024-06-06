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

# Изменение статуса заказа
def change_status():
    selected_item = tree.selection()
    if selected_item:
        order_id = tree.item(selected_item, 'values')[0]
        new_status = status_entry.get()
        conn = sqlite3.connect('business_orders.db')
        cur = conn.cursor()
        cur.execute("UPDATE orders SET status=? WHERE id=?", (new_status, order_id))
        conn.commit()
        conn.close()
        view_orders()
    else:
        messagebox.showwarning("Предупреждение", "Выберите заказ для изменения статуса")

# Анализ заказов (пример)
def analyze_orders():
    # Здесь можно добавить логику анализа заказов
    messagebox.showinfo("Анализ заказов", "Функция анализа заказов пока не реализована")

# Инициализация базы данных
init_db()

# Создание окна приложения
app = tk.Tk()
app.title("Система управления заказами")

# Поля ввода в одну строку
input_frame = tk.Frame(app)
input_frame.pack()

tk.Label(input_frame, text="Имя клиента").grid(row=0, column=0)
customer_name_entry = tk.Entry(input_frame)
customer_name_entry.grid(row=0, column=1)

tk.Label(input_frame, text="Артикул товара").grid(row=0, column=2)
product_sku_entry = tk.Entry(input_frame)
product_sku_entry.grid(row=0, column=3)

tk.Label(input_frame, text="Наименование товара").grid(row=0, column=4)
product_name_entry = tk.Entry(input_frame)
product_name_entry.grid(row=0, column=5)

tk.Label(input_frame, text="Количество").grid(row=0, column=6)
quantity_entry = tk.Entry(input_frame)
quantity_entry.grid(row=0, column=7)

tk.Label(input_frame, text="Дата заказа").grid(row=0, column=8)
order_date_entry = tk.Entry(input_frame)
order_date_entry.grid(row=0, column=9)

tk.Label(input_frame, text="Статус").grid(row=0, column=10)
status_entry = tk.Entry(input_frame)
status_entry.grid(row=0, column=11)

# Кнопка для добавления заказа
add_button = tk.Button(app, text="Добавить заказ", command=add_order)
add_button.pack()

# Кнопка для изменения статуса заказа
status_button = tk.Button(app, text="Изменить статус", command=change_status)
status_button.pack()

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
