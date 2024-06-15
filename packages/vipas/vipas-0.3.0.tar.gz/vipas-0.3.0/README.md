# VIPAS AI Platform SDK
The Vipas AI Python SDK provides a simple and intuitive interface to interact with the Vipas AI platform. This SDK allows you to easily make predictions using pre-trained models hosted on the Vipas AI platform.

## Requirements.

Python 3.7+

## Installation & Usage
### pip install

If the python package is hosted on a repository, you can install directly using:

```sh
pip install git+https://github.com/vipas-engineering/vipas-python-sdk.git
```
(you may need to run `pip` with root permission: `sudo pip install git+https://github.com/vipas-engineering/vipas-python-sdk.git`)

Then import the package:
```python
import vipas
```

### Setuptools

Install via [Setuptools](http://pypi.python.org/pypi/setuptools).

```sh
python setup.py install --user
```
(or `sudo python setup.py install` to install the package for all users)

Then import the package:
```python
import vipas
```

## Getting Started

To get started with the Vipas AI Python SDK, you need to create a ModelClient object and use it to make predictions. Below is a step-by-step guide on how to do this.

### Basic Usage

1. Import the necessary modules:
```python
from vipas import model
```

2. Create a ModelClient object:
```python
vps_model_client = model.ModelClient()
```

3. Make a prediction:

```python
model_id = "mdl-test"
api_response = vps_model_client.predict(model_id=model_id, input_data="Test input")
```

### Handling Exceptions
The SDK provides specific exceptions to handle different error scenarios:

1. UnauthorizedException: Raised when the API key is invalid or missing.
2. NotFoundException: Raised when the model is not found.
3. BadRequestException: Raised when the input data is invalid.
4. ForbiddenException: Raised when the user does not have permission to access the model.
5. ConnectionException: Raised when there is a connection error.
6. RateLimitException: Raised when the rate limit is exceeded.
7. ClientException: Raised when there is a client error.

### Example Usage

```python
from vipas import model
from pprint import pprint
from vipas.exceptions import UnauthorizedException, NotFoundException, ClientException

def main():
    # Create a ModelClient object
    vps_model_client = model.ModelClient()

    # Make a prediction
    try:
        model_id = "model_id"
        api_response = vps_model_client.predict(model_id=model_id, input_data="Test input")
        pprint(api_response)
    except UnauthorizedException as err:
        print(err)
    except NotFoundException as err:
        print(err)
    except ClientException as err:
        print(err)

main()

```

## Logging
The SDK provides a LoggerClient class to handle logging. Here's how you can use it:

### LoggerClient Usage

1. Import the `LoggerClient` class:
```python
from vipas.logger import LoggerClient
```

2. Initialize the `LoggerClient`:
```python
logger = LoggerClient(__name__)

```

3. Log messages at different levels:
```python
logger.debug("This is a debug message")
logger.info("This is an info message")
logger.warning("This is a warning message")
logger.error("This is an error message")
logger.critical("This is a critical message")

```

### Example of LoggerClient
Here is a complete example demonstrating the usage of the LoggerClient:

```python
from vipas.logger import LoggerClient

def main():
    logger = LoggerClient(__name__)
    
    logger.info("Starting the main function")
    
    try:
        # Example operation
        result = 10 / 2
        logger.debug(f"Result of division: {result}")
    except ZeroDivisionError as e:
        logger.error("Error occurred: Division by zero")
    except Exception as e:
        logger.critical(f"Unexpected error: {str(e)}")
    finally:
        logger.info("End of the main function")

main()
``` 

## Author
VIPAS.AI




