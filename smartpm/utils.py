def handle_api_errors(response):
    if response.status_code == 401:
        raise AuthenticationError('Authentication failed')
    elif response.status_code == 404:
        raise NotFoundError('Resource not found')
    elif response.status_code == 429:
        raise RateLimitExceededError('Rate limit exceeded')
    elif response.status_code >= 400:
        raise BadRequestError(f'Bad request: {response.status_code}')
