import sqlite3

def create_cart_table():
    conn = sqlite3.connect('rwow.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cart (
            cart_id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_uid INTEGER,
            item_name TEXT,
            item_count INTEGER,
            FOREIGN KEY(customer_uid) REFERENCES customers(customer_uid)
        )
    ''')
    conn.commit()
    conn.close()

def add_item_to_cart(customer_id, item_name):
    conn = sqlite3.connect('rwow.db')
    cursor = conn.cursor()

    # Check if the item is already in the cart for the customer
    cursor.execute('''
        SELECT item_count FROM cart WHERE customer_uid = ? AND item_name = ?
    ''', (customer_id, item_name))
    result = cursor.fetchone()

    if result:
        # Item already in cart, update the count
        new_count = result[0] + 1
        cursor.execute('''
            UPDATE cart SET item_count = ? WHERE customer_uid = ? AND item_name = ?
        ''', (new_count, customer_id, item_name))
    else:
        # Item not in cart, insert a new row
        new_count = 1
        cursor.execute('''
            INSERT INTO cart (customer_uid, item_name, item_count) VALUES (?, ?, 1)
        ''', (customer_id, item_name))

    conn.commit()
    conn.close()

    return new_count

def get_customer_name(predicted_id):
    conn = sqlite3.connect('rwow.db')
    cursor = conn.cursor()
    cursor.execute("SELECT customer_name FROM customers WHERE customer_uid = ?", (predicted_id,))
    result = cursor.fetchone()
    conn.close()
    if result:
        return result[0]
    else:
        return "Unknown"

def add_ok_sign_column():
    try:
        conn = sqlite3.connect('rwow.db')
        cursor = conn.cursor()
        cursor.execute("ALTER TABLE customers ADD COLUMN ok_sign_detected INTEGER DEFAULT 0")
        conn.commit()
        print("Column 'ok_sign_detected' added successfully.")
    except sqlite3.OperationalError as e:
        print(f"SQLite error: {e}")

def update_ok_sign_detected(predicted_id, ok_sign_detected):
    conn = sqlite3.connect('rwow.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE customers SET ok_sign_detected = ? WHERE customer_uid = ?", (ok_sign_detected, predicted_id))
    conn.commit()
    conn.close()

def fetch_cart_details(customer_id):
    conn = sqlite3.connect('rwow.db')
    cursor = conn.cursor()

    cursor.execute("SELECT customer_name FROM customers WHERE customer_uid = ?", (customer_id,))
    customer_name = cursor.fetchone()[0]

    cursor.execute("SELECT item_name, item_count FROM cart WHERE customer_uid = ?", (customer_id,))
    cart_items = cursor.fetchall()

    conn.close()

    return customer_name, cart_items
