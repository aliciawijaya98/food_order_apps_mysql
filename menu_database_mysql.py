import mysql.connector

# Connect to MySQL server
def get_connection():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",          
        password="admin"   # Change to your MySQL password
    )
    return conn

# Initialize database
def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    # Create a new database if it doesn't exist
    cursor.execute("CREATE DATABASE IF NOT EXISTS restaurant")
    cursor.execute("USE food_menu")  # switch to the newly created database

    # Create the Menu table if it doesn't exist
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS food_menu (
        id INT AUTO_INCREMENT PRIMARY KEY,
        category VARCHAR(50) NOT NULL,
        item VARCHAR(200) NOT NULL,
        price INT UNSIGNED NOT NULL
    )
    ''')

    # Define initial menu data
    food_menu = [
        {"category": "Appetizers", "item": "Spring Rolls", "price": 30000},
        {"category": "Appetizers", "item": "Garlic Bread", "price": 25000},
        {"category": "Appetizers", "item": "Chicken Wings", "price": 40000},
        {"category": "Main Courses", "item": "Grilled Chicken with Rice", "price": 65000},
        {"category": "Main Courses", "item": "Beef Steak", "price": 120000},
        {"category": "Main Courses", "item": "Fried Rice", "price": 45000},
        {"category": "Drinks", "item": "Mineral Water", "price": 10000},
        {"category": "Drinks", "item": "Iced Tea", "price": 15000},
        {"category": "Drinks", "item": "Coffee", "price": 20000},
        {"category": "Desserts", "item": "Ice Cream", "price": 20000},
        {"category": "Desserts", "item": "Chocolate Cake", "price": 30000},
        {"category": "Desserts", "item": "Vanilla Panna Cotta", "price": 40000}
    ]

    # Insert the menu data into the table
    cursor.executemany('''
    INSERT INTO food_menu (category, item, price)
    VALUES (%s, %s, %s)
    ''', [(m['category'], m['item'], m['price']) for m in food_menu])

    # Commit the transaction and close the connection
    conn.commit()

    # Retrieve and print all data from the Menu table
    cursor.execute("SELECT * FROM food_menu")
    for row in cursor.fetchall():
        print(row)

    conn.close()

# Get the database
def get_menu():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM food_menu")
    menus = cursor.fetchall()
    conn.close()
    return menus

# Adding new item to the menu
def add_menu_item(new_item):
    if "category" in new_item and "item" in new_item and "price" in new_item:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO Menu (category, item, price) VALUES (%s, %s, %s)",
            (new_item['category'], new_item['item'], new_item['price'])
        )
        conn.commit()
        conn.close()