import mysql.connector
from mysql.connector import Error

def get_connection():
    try:
        conn = mysql.connector.connect(
            host="127.0.0.1",  #IP lebih stabil
            user="root",
            password="Admin@123.",
            database="restaurant",
            port=3306
        )

        return conn

    except Error as e:
        print("[DB ERROR]", e)
        return None