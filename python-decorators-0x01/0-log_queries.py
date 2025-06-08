import sqlite3
import functools

#### decorator to log SQL queries

def log_queries(func):
    """
    Decorator that logs SQL queries before executing them.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Look for query in positional arguments
        if args:
            query = args[0]
            print(f"Executing SQL query: {query}")
        # Look for query in keyword arguments
        elif 'query' in kwargs:
            query = kwargs['query']
            print(f"Executing SQL query: {query}")
        else:
            print("Warning: No SQL query found in function arguments")
        
        # Execute the original function
        return func(*args, **kwargs)
    return wrapper

@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

#### fetch users while logging the query
users = fetch_all_users(query="SELECT * FROM users")
