import streamlit as st
import sqlite3

# Styling configuration
class CommonStyling:
    def __init__(self):
        self.bg_color = "#E0F7FA"
        self.frame_bg_color = "#00796B"
        self.font_heading = ("Helvetica", 24, "bold")
        self.font_label = ("Helvetica", 12)
        self.fg_color = "#004D40"

# Initialize styling
styling = CommonStyling()

# Initialize database
def init_db():
    conn = sqlite3.connect('restaurant.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            contact TEXT NOT NULL,
            address TEXT NOT NULL,
            order_price TEXT NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY,
            table_number INTEGER NOT NULL,
            order_price REAL NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# User authentication
def authenticate(username, password):
    return username == "admin" and password == "password"

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    with st.form("login_form"):
        st.markdown("<h1 style='text-align: center;'>BAWARCHIES</h1>", unsafe_allow_html=True)
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit_button = st.form_submit_button("Login")

        if submit_button:
            if authenticate(username, password):
                st.session_state.authenticated = True
                st.success("Login successful!")
            else:
                st.error("Invalid username or password")

if st.session_state.authenticated:
    st.sidebar.title("Bawarchies Ordering System")
    page = st.sidebar.radio("Navigation", ["Menu", "Customer Details", "Order Allotment", "Logout"])

    if page == "Menu":
        st.title("Menu")
        menu_items = [("Pizza", 150), ("Burger", 95), ("Pasta", 79), ("Sandwich", 89), ("French Fries", 99)]
        order_items = []

        for item in menu_items:
            item_name, item_price = item
            st.write(f"{item_name} - {item_price} Rs")
            quantity = st.number_input(f"Quantity for {item_name}", min_value=0, max_value=10, step=1, key=item_name)
            if quantity > 0:
                order_items.append((item_name, item_price, quantity))

        if st.button("Add to Order"):
            st.session_state.order_items = order_items
            st.success("Items added to order")

        if "order_items" in st.session_state:
            total = sum(item[1] * item[2] for item in st.session_state.order_items)
            st.write(f"Total: {total} Rs")
            table_number = st.number_input("Table Number", min_value=1, step=1)
            if st.button("Process Payment"):
                if table_number:
                    try:
                        conn = sqlite3.connect('restaurant.db')
                        cursor = conn.cursor()
                        cursor.execute('INSERT INTO orders (table_number, order_price) VALUES (?, ?)', (table_number, total))
                        conn.commit()
                        conn.close()
                        st.success("Order details stored successfully!")
                    except Exception as e:
                        st.error(f"An error occurred while storing order details: {e}")

    elif page == "Customer Details":
        st.title("Customer Details")

        conn = sqlite3.connect('restaurant.db')
        cursor = conn.cursor()
        cursor.execute('SELECT id, name, contact, address, order_price FROM customers')
        customers = cursor.fetchall()
        conn.close()

        st.table(customers)

        with st.form("add_customer_form"):
            name = st.text_input("Name")
            contact = st.text_input("Contact")
            address = st.text_input("Address")
            order_price = st.text_input("Order Price")
            add_button = st.form_submit_button("Add Customer")

            if add_button:
                if name and contact and address and order_price:
                    try:
                        conn = sqlite3.connect('restaurant.db')
                        cursor = conn.cursor()
                        cursor.execute('INSERT INTO customers (name, contact, address, order_price) VALUES (?, ?, ?, ?)',
                                       (name, contact, address, order_price))
                        conn.commit()
                        conn.close()
                        st.success("Customer added successfully!")
                    except Exception as e:
                        st.error(f"An error occurred while adding the customer: {e}")

    elif page == "Order Allotment":
        st.title("Order Allotment")

        conn = sqlite3.connect('restaurant.db')
        cursor = conn.cursor()
        cursor.execute('SELECT table_number, order_price FROM orders')
        orders = cursor.fetchall()
        conn.close()

        st.table(orders)

    elif page == "Logout":
        st.session_state.authenticated = False
        st.success("Logged out successfully!")
        st.experimental_rerun()
