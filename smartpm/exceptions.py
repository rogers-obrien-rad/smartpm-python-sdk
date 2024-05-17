class SmartPMError(Exception):
    """Base class for all exceptions raised by the SmartPM SDK."""
    pass

class AuthenticationError(SmartPMError):
    """Exception raised for authentication errors."""
    pass

class NotFoundError(SmartPMError):
    """Exception raised when a requested resource is not found."""
    pass

class RateLimitExceededError(SmartPMError):
    """Exception raised when the rate limit is exceeded."""
    pass

class BadRequestError(SmartPMError):
    """Exception raised for bad requests (status code 400)."""
    pass

class NoCommentsFoundError(NotFoundError):
    """Exception raised when no comments are found for a project."""
    pass
