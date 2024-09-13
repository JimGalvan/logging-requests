
# LoggingRequests

`LoggingRequests` is a Python wrapper for the `requests` library that provides enhanced logging capabilities for HTTP requests and responses. This library allows you to log details such as request headers, body content, and responses, making it useful for debugging and monitoring HTTP traffic in your application.

## Features

- Logs HTTP requests and responses with custom log levels.
- Supports logging of request headers, parameters, JSON body, and response data.
- Allows specifying URLs to exclude from logging.
- Supports GET, POST, PATCH, PUT, and DELETE requests.
- Optionally log requests and/or responses.
- Flexible logger integration with support for custom loggers.

## Installation

1. Clone this repository:

    ```bash
    git clone https://github.com/your-username/logging-requests.git
    ```

2. Navigate to the project directory:

    ```bash
    cd logging-requests
    ```

3. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

    If `requests` is not listed in `requirements.txt`, you can manually install it:

    ```bash
    pip install requests
    ```

## Usage

### Basic Usage

Here’s a simple example of how to use `LoggingRequests`:

```python
from logging_requests import LoggingRequests

# Initialize LoggingRequests
logging_requests = LoggingRequests()

# Make a GET request
response = logging_requests.get("https://jsonplaceholder.typicode.com/posts")
```

### Custom Logger

You can pass a custom logger to the `LoggingRequests` class if you want more control over the logging configuration.

```python
import logging
from logging_requests import LoggingRequests

# Create a custom logger
custom_logger = logging.getLogger('my_custom_logger')
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
custom_logger.addHandler(handler)
custom_logger.setLevel(logging.INFO)

# Initialize LoggingRequests with the custom logger
logging_requests = LoggingRequests(logger=custom_logger)

# Make a POST request
response = logging_requests.post("https://jsonplaceholder.typicode.com/posts", json={"title": "foo", "body": "bar", "userId": 1})
```

### Ignoring Certain Paths from Logging

You can specify paths that should be ignored from logging:

```python
ignore_paths = ["/ignore-this-path"]

# Initialize LoggingRequests with paths to ignore
logging_requests = LoggingRequests(paths_to_ignore=ignore_paths)

# Any requests to URLs containing "/ignore-this-path" will not be logged
response = logging_requests.get("https://example.com/ignore-this-path")
```

### Custom Log Levels

You can set the log level for requests and responses. By default, it logs at `logging.INFO`, but you can adjust it:

```python
from logging_requests import LoggingRequests
import logging

# Initialize LoggingRequests with a custom log level
logging_requests = LoggingRequests(log_level=logging.DEBUG)

# Make a GET request with detailed logs
response = logging_requests.get("https://jsonplaceholder.typicode.com/posts")
```

### Enabling/Disabling Request/Response Logging

You can control whether requests and/or responses are logged by passing flags `log_requests` and `log_responses`:

```python
# Only log responses, but not requests
logging_requests = LoggingRequests(log_requests=False, log_responses=True)

response = logging_requests.get("https://jsonplaceholder.typicode.com/posts")
```

## Methods

- `get(url, *args, **kwargs)`: Send a GET request.
- `post(url, *args, **kwargs)`: Send a POST request.
- `put(url, *args, **kwargs)`: Send a PUT request.
- `patch(url, *args, **kwargs)`: Send a PATCH request.
- `delete(url, *args, **kwargs)`: Send a DELETE request.

All methods support additional arguments and keyword arguments, which are passed directly to the underlying `requests.request` function.

## Example Log Output

Here's an example of the log output:

```
==================================================
START REQUEST
==================================================
Request: GET https://jsonplaceholder.typicode.com/posts
END REQUEST
==================================================
START RESPONSE
==================================================
Response status code: 200
Response headers:
{'Content-Type': 'application/json; charset=utf-8'}
Response content:
[
    {
        "userId": 1,
        "id": 1,
        "title": "sample title",
        "body": "sample body"
    }
]
END RESPONSE
==================================================
```

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue.

### Running Tests

To run tests, ensure you have `pytest` installed and run:

```bash
pytest
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
