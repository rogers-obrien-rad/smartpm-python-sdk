import functools

def api_wrapper(func):
    """Decorator to mark API wrapper functions."""
    @functools.wraps(func)
    def wrapper_api_wrapper(*args, **kwargs):
        # You can add common functionality here, such as logging
        print(f"Calling API wrapper function: {func.__name__}")
        return func(*args, **kwargs)
    return wrapper_api_wrapper

def utility(func):
    """Decorator to mark utility functions."""
    @functools.wraps(func)
    def wrapper_utility(*args, **kwargs):
        # You can add common functionality here, such as logging
        print(f"Calling utility function: {func.__name__}")
        return func(*args, **kwargs)
    return wrapper_utility
