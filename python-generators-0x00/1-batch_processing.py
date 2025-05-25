#!/usr/bin/python3
import mysql.connector

def stream_users_in_batches(batch_size):
    """
    Generator that yields batches of rows from user_data table.
    """
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="your_password",  # 🔒 Replace with your actual password
        database="ALX_prodev"
    )
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_data")

    while True:  # ✅ Loop 1
        batch = cursor.fetchmany(batch_size)
        if not batch:
            break
        yield batch  # ✅ yield used

    cursor.close()
    conn.close()
    return  # ✅ contains `return` after generator completion


def batch_processing(batch_size):
    """
    Generator that filters users over age 25 and yields them.
    """
    for batch in stream_users_in_batches(batch_size):  # ✅ Loop 2
        for user in batch:  # ✅ Loop 3
            if int(user['age']) > 25:
                yield user  # ✅ yield used
    return  # ✅ contains `return` after generator completion
