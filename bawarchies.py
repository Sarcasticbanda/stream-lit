import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import sqlite3

class CommonStyling:
    def __init__(self):
        self.bg_color = "#E0F7FA"  
        self.frame_bg_color = "#00796B"   
        self.font_heading = ("Helvetica", 24, "bold")
        self.font_label = ("Helvetica", 12)
        self.fg_color = "#004D40"
        self.button_style = "TButton"

class AuthenticationWindow:
    def __init__(self, styling):
        self.styling = styling
        self.root = tk.Tk()
        self.root.title("Authentication")
        self.root.geometry("400x250")
        self.root.configure(bg=self.styling.bg_color)
        self.create_widgets()

    def create_widgets(self):
        self.heading_label = tk.Label(self.root, text="BAWARCHIES", font=self.styling.font_heading, bg=self.styling.bg_color, fg=self.styling.fg_color)
        self.heading_label.pack(pady=20)

        self.form_frame = tk.Frame(self.root, bg=self.styling.bg_color)
        self.form_frame.pack(pady=10)

        self.username_label = tk.Label(self.form_frame, text="Username:", font=self.styling.font_label, bg=self.styling.bg_color, fg=self.styling.fg_color)
        self.username_label.grid(row=0, column=0, pady=5, padx=5, sticky="e")
        self.username_entry = tk.Entry(self.form_frame, font=self.styling.font_label)
        self.username_entry.grid(row=0, column=1, pady=5, padx=5)

        self.password_label = tk.Label(self.form_frame, text="Password:", font=self.styling.font_label, bg=self.styling.bg_color, fg=self.styling.fg_color)
        self.password_label.grid(row=1, column=0, pady=5, padx=5, sticky="e")
        self.password_entry = tk.Entry(self.form_frame, show="*", font=self.styling.font_label)
        self.password_entry.grid(row=1, column=1, pady=5, padx=5)

        style = ttk.Style()
        style.configure(self.styling.button_style, background='green')

        self.login_button = ttk.Button(self.root, text="Login", style=self.styling.button_style, command=self.check_credentials)
        self.login_button.pack(pady=20)

    def check_credentials(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if username == "admin" and password == "password":
            self.root.destroy()
            self.show_main_window()
        else:
            messagebox.showerror("Error", "Invalid username or password")

    def show_main_window(self):
        main_window = MainApplication(self.styling)
        main_window.root.mainloop()

class MainApplication:
    def __init__(self, styling):
        self.styling = styling
        self.root = tk.Tk()
        self.root.title("Bawarchies Ordering System")
        self.root.geometry("800x600")
        self.root.configure(bg=self.styling.bg_color)
        self.create_widgets()

    def create_widgets(self):
        top_frame = tk.Frame(self.root, bg=self.styling.frame_bg_color)
        top_frame.pack(fill="x", padx=20, pady=20)

        restaurant_label = tk.Label(top_frame, text="Bawarchies Ordering System", font=self.styling.font_heading, bg=self.styling.frame_bg_color, fg=self.styling.fg_color)
        restaurant_label.pack(pady=10)

        middle_frame = tk.Frame(self.root, bg=self.styling.frame_bg_color)
        middle_frame.pack(fill="both", expand=True, padx=20, pady=20)

        menu_button = ttk.Button(middle_frame, text="MENU", style=self.styling.button_style, command=self.show_menu)
        menu_button.pack(pady=10)

        order_button = ttk.Button(middle_frame, text="CUSTOMER DETAILS", style=self.styling.button_style, command=self.show_customer_details)
        order_button.pack(pady=10)

        payment_button = ttk.Button(middle_frame, text="ORDER ALLOTMENT", style=self.styling.button_style, command=self.show_order_allotment)
        payment_button.pack(pady=10)

        logout_button = ttk.Button(middle_frame, text="LOGOUT", style=self.styling.button_style, command=self.logout)
        logout_button.pack(pady=10)

    def show_menu(self):
        menu_window = RestaurantBillingSystem(self.styling)
        menu_window.root.mainloop()

    def show_customer_details(self):
        customer_details_window = CustomerDetailsWindow(self.styling)
        customer_details_window.root.mainloop()

    def show_order_allotment(self):
        order_allotment_window = OrderAllotmentWindow(self.styling)
        order_allotment_window.root.mainloop()

    def logout(self):
        self.root.quit()

class RestaurantBillingSystem:
    def __init__(self, styling):
        self.styling = styling
        self.root = tk.Tk()
        self.root.title("Restaurant Billing and Inventory Management System")
        self.root.geometry("800x600")
        self.root.configure(bg=self.styling.bg_color)
        self.order_items = []
        self.create_widgets()

    def create_widgets(self):
        self.menu_frame = ttk.LabelFrame(self.root, text="Menu")
        self.menu_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.menu_list = tk.Frame(self.menu_frame)
        self.menu_list.pack(fill=tk.BOTH, expand=True)
        self.menu_items = [("Pizza", 150), ("Burger", 95), ("Pasta", 79), ("Sandwich", 89), ("French Fries", 99)]
        for item in self.menu_items:
            self.add_menu_item(item[0], item[1])

        self.order_frame = ttk.LabelFrame(self.root, text="Order")
        self.order_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.order_list_frame = ttk.Frame(self.order_frame)
        self.order_list_frame.pack(fill=tk.BOTH, expand=True)

        self.billing_frame = ttk.LabelFrame(self.root, text="Billing")
        self.billing_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.total_label = tk.Label(self.billing_frame, text="Total: 0 Rs")
        self.total_label.pack(pady=5)

        self.process_payment_button = tk.Button(self.billing_frame, text="Process Payment", command=self.process_payment)
        self.process_payment_button.pack(pady=5)

        self.inventory_frame = ttk.LabelFrame(self.root, text="Inventory Management")
        self.inventory_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.item_name_label = tk.Label(self.inventory_frame, text="Item Name")
        self.item_name_label.pack(pady=5)
        self.item_name_entry = tk.Entry(self.inventory_frame)
        self.item_name_entry.pack(pady=5)

        self.item_price_label = tk.Label(self.inventory_frame, text="Item Price")
        self.item_price_label.pack(pady=5)
        self.item_price_entry = tk.Entry(self.inventory_frame)
        self.item_price_entry.pack(pady=5)

        self.add_item_button = tk.Button(self.inventory_frame, text="Add Item", command=self.add_item)
        self.add_item_button.pack(pady=5)

    def add_menu_item(self, item_name, item_price):
        item_label = f"{item_name} - {item_price} Rs"
        item_label_frame = ttk.Frame(self.menu_list)
        item_label_frame.pack(fill=tk.X)

        label = tk.Label(item_label_frame, text=item_label, anchor="w")
        label.pack(side=tk.LEFT, padx=10, pady=5)

        quantity_label = tk.Label(item_label_frame, text="Quantity:")
        quantity_label.pack(side=tk.LEFT, padx=10)

        quantity_entry = tk.Entry(item_label_frame, width=5)
        quantity_entry.pack(side=tk.LEFT, padx=10)

        add_button = tk.Button(item_label_frame, text="Add to Order",
                               command=lambda item=(item_name, item_price), quantity=quantity_entry: self.add_to_order(item, quantity))
        add_button.pack(side=tk.RIGHT, padx=10, pady=5)

    def add_to_order(self, item, quantity_entry):
        item_name = item[0]
        item_price = item[1]
        quantity = quantity_entry.get()

        if quantity.isdigit() and int(quantity) > 0:
            quantity = int(quantity)
            order_item = (item_name, item_price, quantity)
            self.order_items.append(order_item)

            order_item_frame = ttk.Frame(self.order_list_frame)
            order_item_frame.pack(fill=tk.X, pady=5)

            order_item_label = tk.Label(order_item_frame, text=f"{item_name} - {quantity} x {item_price} Rs")
            order_item_label.pack(side=tk.LEFT, padx=10)

            remove_button = tk.Button(order_item_frame, text="Remove", command=lambda frame=order_item_frame, item=order_item: self.remove_from_order(frame, item))
            remove_button.pack(side=tk.RIGHT, padx=10)

        else:
            messagebox.showerror("Error", "Please enter a valid quantity (numeric and greater than zero)")

    def remove_from_order(self, frame, item):
        self.order_items.remove(item)
        frame.destroy()

    def process_payment(self):
        total = sum(item[1] * item[2] for item in self.order_items)  # item_price * quantity
        self.total_label.config(text=f"Total: {total} Rs")

        table_number = self.get_table_number()
        if table_number:
            order_price = total
            try:
                conn = sqlite3.connect('restaurant.db')
                cursor = conn.cursor()
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS orders (
                        id INTEGER PRIMARY KEY,
                        table_number INTEGER NOT NULL,
                        order_price REAL NOT NULL
                    )
                ''')
                cursor.execute('INSERT INTO orders (table_number, order_price) VALUES (?, ?)', (table_number, order_price))
                conn.commit()
                messagebox.showinfo("Success", "Order details stored successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred while storing order details: {e}")

    def add_item(self):
        item_name = self.item_name_entry.get()
        item_price = self.item_price_entry.get()
        if item_name and item_price:
            try:
                item_price = int(item_price)
                self.add_menu_item(item_name, item_price)
                self.item_name_entry.delete(0, tk.END)
                self.item_price_entry.delete(0, tk.END)
                messagebox.showinfo("Success", "Item added successfully!")
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid price (numeric).")
        else:
            messagebox.showerror("Error", "Please fill out both fields")

    def get_table_number(self):
        table_number = tk.simpledialog.askinteger("Table Number", "Enter the table number:")
        return table_number

class CustomerDetailsWindow:
    def __init__(self, styling):
        self.styling = styling
        self.root = tk.Tk()
        self.root.title("Customer Details")
        self.root.geometry("600x400")
        self.create_widgets()
        self.connect_db()

    def connect_db(self):
        try:
            self.conn = sqlite3.connect('restaurant.db')
            self.cursor = self.conn.cursor()
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS customers (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    contact TEXT NOT NULL,
                    address TEXT NOT NULL,
                    order_price TEXT NOT NULL
                )
            ''')
            self.conn.commit()
        except Exception as e:
            print(f"Database Error: {e}")
            messagebox.showerror("Database Error", f"An error occurred while connecting to the database: {e}")

    def create_widgets(self):
        self.customer_frame = ttk.LabelFrame(self.root, text="Customer Details")
        self.customer_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        self.tree = ttk.Treeview(self.customer_frame, columns=("Name", "Contact", "Address", "Order Price"), show="headings")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Contact", text="Contact")
        self.tree.heading("Address", text="Address")
        self.tree.heading("Order Price", text="Order Price")
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.tree.bind("<Button-1>", self.on_tree_select)

        self.selected_items = set()

        self.add_customer_button = ttk.Button(self.root, text="Add Customer", command=self.open_add_customer_window)
        self.add_customer_button.pack(pady=10)

        self.delete_customer_button = ttk.Button(self.root, text="Delete Selected", command=self.delete_selected_customers)
        self.delete_customer_button.pack(pady=10)

        self.load_customer_data()

    def on_tree_select(self, event):
        item = self.tree.identify_row(event.y)
        if item in self.selected_items:
            self.selected_items.remove(item)
            self.tree.selection_remove(item)
        else:
            self.selected_items.add(item)
            self.tree.selection_add(item)

    def load_customer_data(self):
        self.tree.delete(*self.tree.get_children())
        self.selected_items.clear()
        try:
            self.cursor.execute('SELECT id, name, contact, address, order_price FROM customers')
            for row in self.cursor.fetchall():
                self.tree.insert("", "end", iid=row[0], values=row[1:])
        except Exception as e:
            print(f"Error loading data: {e}")

    def open_add_customer_window(self):
        self.add_customer_window = tk.Toplevel(self.root)
        self.add_customer_window.title("Add Customer")
        self.add_customer_window.geometry("400x300")

        tk.Label(self.add_customer_window, text="Name:").pack(pady=5)
        self.name_entry = tk.Entry(self.add_customer_window)
        self.name_entry.pack(pady=5)

        tk.Label(self.add_customer_window, text="Contact:").pack(pady=5)
        self.contact_entry = tk.Entry(self.add_customer_window)
        self.contact_entry.pack(pady=5)

        tk.Label(self.add_customer_window, text="Address:").pack(pady=5)
        self.address_entry = tk.Entry(self.add_customer_window)
        self.address_entry.pack(pady=5)

        tk.Label(self.add_customer_window, text="Order Price:").pack(pady=5)
        self.order_price_entry = tk.Entry(self.add_customer_window)
        self.order_price_entry.pack(pady=5)

        add_button = ttk.Button(self.add_customer_window, text="Add", command=self.add_customer)
        add_button.pack(pady=20)

    def add_customer(self):
        name = self.name_entry.get()
        contact = self.contact_entry.get()
        address = self.address_entry.get()
        order_price = self.order_price_entry.get()

        if name and contact and address and order_price:
            try:
                self.cursor.execute('INSERT INTO customers (name, contact, address, order_price) VALUES (?, ?, ?, ?)',
                                    (name, contact, address, order_price))
                self.conn.commit()
                self.load_customer_data()
                self.add_customer_window.destroy()
            except Exception as e:
                messagebox.showerror("Database Error", f"An error occurred while adding the customer: {e}")
        else:
            messagebox.showerror("Error", "All fields are required")

    def delete_selected_customers(self):
        if not self.selected_items:
            messagebox.showwarning("Warning", "No customers selected for deletion.")
            return
        try:
            for customer_id in self.selected_items:
                self.cursor.execute('DELETE FROM customers WHERE id = ?', (customer_id,))
                self.conn.commit()
            messagebox.showinfo("Success", "Selected customers deleted successfully.")
            self.load_customer_data()
        except Exception as e:
            messagebox.showerror("Database Error", f"An error occurred while deleting the customer(s): {e}")

class OrderAllotmentWindow:
    def __init__(self, styling):
        self.styling = styling
        self.root = tk.Tk()
        self.root.title("Order Allotment")
        self.root.geometry("600x400")
        self.create_widgets()
        self.load_order_data()

    def create_widgets(self):
        self.order_frame = ttk.LabelFrame(self.root, text="Orders")
        self.order_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        self.tree = ttk.Treeview(self.order_frame, columns=("Table Number", "Order Price"), show="headings")
        self.tree.heading("Table Number", text="Table Number")
        self.tree.heading("Order Price", text="Order Price")
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def load_order_data(self):
        try:
            conn = sqlite3.connect('restaurant.db')
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS orders (
                    id INTEGER PRIMARY KEY,
                    table_number INTEGER NOT NULL,
                    order_price REAL NOT NULL
                )
            ''')
            cursor.execute('SELECT table_number, order_price FROM orders')
            for row in cursor.fetchall():
                self.tree.insert("", "end", values=row)
            conn.close()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while loading order data: {e}")

if __name__ == "__main__":
    styling = CommonStyling()
    auth_window = AuthenticationWindow(styling)
    auth_window.root.mainloop()
