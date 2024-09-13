import json
import requests
import logging
from typing import Optional

class LoggingRequests:
    def __init__(self, logger: Optional[logging.Logger] = None, log_level=logging.INFO, paths_to_ignore=None, log_requests=True, log_responses=True):
        self.logger = logger or logging.getLogger(__name__)
        self.log_level = log_level
        self.paths_to_ignore = paths_to_ignore or []
        self.log_requests = log_requests
        self.log_responses = log_responses

    def _log_request(self, method, url, **kwargs):
        if self.log_requests:
            self.logger.log(self.log_level, "=" * 50)
            self.logger.log(self.log_level, "START REQUEST")
            self.logger.log(self.log_level, "=" * 50)
            self.logger.log(self.log_level, f"Request: {method} {url}")
            
            if 'headers' in kwargs:
                self.logger.log(self.log_level, f"Request headers:\n{kwargs['headers']}")
            if 'params' in kwargs:
                self.logger.log(self.log_level, f"Request params:\n{kwargs['params']}")
            if 'json' in kwargs:
                self.logger.log(self.log_level, f"Request JSON:\n{json.dumps(kwargs['json'], indent=4)}")
            if 'data' in kwargs:
                self._log_data(kwargs['data'])

    def _log_data(self, data):
        if isinstance(data, dict):
            self.logger.log(self.log_level, f"Request data:\n{json.dumps(data, indent=4)}")
        elif isinstance(data, str):
            try:
                data_json = json.loads(data)
                self.logger.log(self.log_level, f"Request data:\n{json.dumps(data_json, indent=4)}")
            except json.JSONDecodeError:
                self.logger.log(self.log_level, f"Request data:\n{data}")
        else:
            self.logger.log(self.log_level, f"Request data:\n{str(data)}")

    def _log_response(self, response):
        if self.log_responses:
            self.logger.log(self.log_level, "=" * 50)
            self.logger.log(self.log_level, "START RESPONSE")
            self.logger.log(self.log_level, "=" * 50)
            self.logger.log(self.log_level, f"Response status code: {response.status_code}")
            
            if not any(path in response.url for path in self.paths_to_ignore):
                self.logger.log(self.log_level, f"Response headers:\n{response.headers}")
                content_type = response.headers.get('Content-Type', '')
                if 'application/json' in content_type:
                    try:
                        content = response.json()
                        pretty_content = json.dumps(content, indent=4)
                    except ValueError:
                        pretty_content = response.text
                else:
                    pretty_content = response.text
                self.logger.log(self.log_level, f"Response content:\n{pretty_content}")

    def request(self, method, url, *args, **kwargs):
        self._log_request(method, url, **kwargs)
        
        # Make the request
        response = requests.request(method, url, *args, **kwargs)
        
        # Log the end of the request
        self.logger.log(self.log_level, "END REQUEST")
        self.logger.log(self.log_level, "=" * 50)

        self._log_response(response)
        
        # Log the end of the response
        self.logger.log(self.log_level, "END RESPONSE")
        self.logger.log(self.log_level, "=" * 50)

        return response

    def get(self, url, *args, **kwargs):
        return self.request('GET', url, *args, **kwargs)

    def post(self, url, *args, **kwargs):
        return self.request('POST', url, *args, **kwargs)

    def patch(self, url, *args, **kwargs):
        return self.request('PATCH', url, *args, **kwargs)

    def delete(self, url, *args, **kwargs):
        return self.request('DELETE', url, *args, **kwargs)

    def put(self, url, *args, **kwargs):
        return self.request('PUT', url, *args, **kwargs)
