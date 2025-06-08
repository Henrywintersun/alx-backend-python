import sqlite3 
import functools

def with_db_connection(func):
    """
    Decorator that automatically opens and closes database connections.
    Passes the connection as the first argument to the decorated function.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Open database connection
        conn = sqlite3.connect('users.db')
        try:
            # Call the original function with connection as first argument
            result = func(conn, *args, **kwargs)
            return result
        finally:
            # Always close the connection
            conn.close()
    return wrapper

def transactional(func):
    """
    Decorator that manages database transactions by automatically committing or rolling back changes.
    If the function raises an error, rollback; otherwise commit the transaction.
    Expects the connection to be the first argument of the decorated function.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Get the connection (should be first argument)
        if args:
            conn = args[0]
        else:
            raise ValueError("Connection must be the first argument")
        
        try:
            # Execute the function
            result = func(*args, **kwargs)
            # If successful, commit the transaction
            conn.commit()
            return result
        except Exception as e:
            # If error occurs, rollback the transaction
            conn.rollback()
            raise e
    return wrapper

@with_db_connection 
@transactional 
def update_user_email(conn, user_id, new_email): 
    cursor = conn.cursor() 
    cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id)) 

#### Update user's email with automatic transaction handling 
update_user_email(user_id=1, new_email='Crawford_Cartwright@hotmail.com')
