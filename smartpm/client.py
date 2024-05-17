import requests
from smartpm.exceptions import SmartPMError, AuthenticationError, NotFoundError, RateLimitExceededError, BadRequestError, NoCommentsFoundError

class SmartPMClient:
    BASE_URL = 'https://live.smartpmtech.com/public/v1'

    def __init__(self, api_key, company_id):
        self.api_key = api_key
        self.company_id = company_id
        self.headers = {
            'X-API-KEY': self.api_key,
            'X-COMPANY-ID': self.company_id
        }

    def _get(self, endpoint, params=None):
        url = f'{self.BASE_URL}/{endpoint}'
        response = requests.get(url, headers=self.headers, params=params)
        self._handle_response(response)
        return response.json()

    def _post(self, endpoint, data=None):
        url = f'{self.BASE_URL}/{endpoint}'
        response = requests.post(url, headers=self.headers, json=data)
        self._handle_response(response)
        return response.json()

    def _put(self, endpoint, data=None):
        url = f'{self.BASE_URL}/{endpoint}'
        response = requests.put(url, headers=self.headers, json=data)
        self._handle_response(response)
        return response.json()

    def _delete(self, endpoint):
        url = f'{self.BASE_URL}/{endpoint}'
        response = requests.delete(url, headers=self.headers)
        self._handle_response(response)
        return response.status_code == 204

    def _handle_response(self, response):
        if response.status_code == 401:
            raise AuthenticationError('Authentication failed')
        elif response.status_code == 404:
            # Check if the 404 is for comments
            if 'comments' in response.request.url:
                raise NoCommentsFoundError('No comments found for this project.')
            else:
                raise NotFoundError('Resource not found')
        elif response.status_code == 429:
            raise RateLimitExceededError('Rate limit exceeded')
        elif response.status_code >= 400:
            raise BadRequestError(f'Bad request: {response.status_code}')
        if not response.ok:
            raise SmartPMError(f'API request failed with status {response.status_code}: {response.text}')
