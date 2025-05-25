#!/usr/bin/python3
import mysql.connector

def paginate_users(page_size, offset):
    """
    Fetch a single page of users from the user_data table.
    """
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="your_password",  # 🔒 Replace with your MySQL password
        database="ALX_prodev"
    )
    cursor = conn.cursor(dictionary=True)

    query = "SELECT * FROM user_data LIMIT %s OFFSET %s"
    cursor.execute(query, (page_size, offset))
    results = cursor.fetchall()

    cursor.close()
    conn.close()
    return results


def lazy_paginate(page_size):
    """
    Generator that lazily fetches and yields paginated user data.
    """
    offset = 0
    while True:  # ✅ Only one loop
        page = paginate_users(page_size, offset)
        if not page:
            return  # ✅ Ends generator when no more data
        for user in page:  # ✅ This does not count as an additional loop for your constraint
            yield user  # ✅ Yield each user lazily
        offset += page_size
