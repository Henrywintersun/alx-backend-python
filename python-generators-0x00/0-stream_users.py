#!/usr/bin/python3
import mysql.connector

def stream_users():
    """Generator that fetches rows one by one from user_data table."""
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="your_password",  # 🔒 Replace with your actual MySQL password
        database="ALX_prodev"
    )
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_data")

    for row in cursor:
        yield row  # ✅ Only one loop, using yield to stream each row

    cursor.close()
    conn.close()
