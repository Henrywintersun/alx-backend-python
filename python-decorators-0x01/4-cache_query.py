import time
import sqlite3 
import functools

query_cache = {}

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

def cache_query(func):
    """
    Decorator that caches query results based on the SQL query string
    to avoid redundant database calls.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Create cache key from function arguments (excluding connection)
        cache_key_parts = []
        
        # Add positional arguments (skip connection object)
        for i, arg in enumerate(args):
            if hasattr(arg, 'execute'):  # Skip connection objects
                continue
            cache_key_parts.append(str(arg))
        
        # Add keyword arguments
        for key, value in sorted(kwargs.items()):
            cache_key_parts.append(f"{key}={value}")
        
        # Create cache key
        cache_key = "|".join(cache_key_parts)
        
        # Check if result is already cached
        if cache_key in query_cache:
            print(f"Cache HIT: Using cached result for key: {cache_key}")
            return query_cache[cache_key]
        
        # Execute function and cache result
        print(f"Cache MISS: Executing query and caching result for key: {cache_key}")
        result = func(*args, **kwargs)
        
        # Store result in global cache
        query_cache[cache_key] = result
        
        return result
    
    return wrapper

@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

#### First call will cache the result
users = fetch_users_with_cache(query="SELECT * FROM users")

#### Second call will use the cached result
users_again = fetch_users_with_cache(query="SELECT * FROM users")
