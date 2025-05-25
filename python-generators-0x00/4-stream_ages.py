#!/usr/bin/python3
import mysql.connector

def stream_user_ages():
    """
    Generator that yields user ages one by one from the user_data table.
    """
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="your_password",  # Replace with your MySQL password
        database="ALX_prodev"
    )
    cursor = conn.cursor()
    cursor.execute("SELECT age FROM user_data")

    for (age,) in cursor:  # ✅ Loop 1
        yield int(age)

    cursor.close()
    conn.close()


def calculate_average_age():
    """
    Uses the age generator to compute the average age.
    """
    total_age = 0
    count = 0

    for age in stream_user_ages():  # ✅ Loop 2
        total_age += age
        count += 1

    if count == 0:
        print("No users found.")
    else:
        average = total_age / count
        print(f"Average age of users: {average:.2f}")


if __name__ == "__main__":
    calculate_average_age()
