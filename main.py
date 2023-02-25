import json
import logging
from typing import Tuple
import functions_framework

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def hello(name):
    """This function returns a greeting message.
    It is called by the main function.
    """
    logging.info("Hello function called.")
    return "Hello {}!".format(name)


@functions_framework.http
def main(request) -> Tuple[str, int]:
    """This function is the entry point for the cloud function.
    It parses the request body and calls the appropriate function.
    Then it returns the result of the function call as HTTP response.
    """
    # Parse the request body
    request_json = request.get_json(silent=True)
    request_args = request.args

    if request_json and "name" in request_json:
        name = request_json["name"]
    elif request_args and "name" in request_args:
        name = request_args["name"]
    else:
        name = "World"

    # Call the function
    result = hello(name)

    # Return the result as HTTP response
    return json.dumps(result), 200
