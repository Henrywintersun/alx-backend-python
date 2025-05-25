#!/usr/bin/python3
import mysql.connector

def stream_users_in_batches(batch_size):
    """
    Generator that yields batches of rows from the user_data table.
    """
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="your_password",  # 🔒 Replace with your actual password
        database="ALX_prodev"
    )
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_data")

    while True:
        batch = cursor.fetchmany(batch_size)
        if not batch:
            break
        yield batch  # ✅ First loop (inside generator)

    cursor.close()
    conn.close()

def batch_processing(batch_size):
    """
    Generator that processes batches and yields users over age 25.
    """
    for batch in stream_users_in_batches(batch_size):  # ✅ Second loop
        filtered_users = [user for user in batch if int(user['age']) > 25]  # ✅ Third loop (list comprehension)
        yield filtered_users
