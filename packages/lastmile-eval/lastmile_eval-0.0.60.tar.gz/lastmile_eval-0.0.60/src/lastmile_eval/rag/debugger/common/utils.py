"""
Utils file for various needs in the RAG debugger.
"""

import requests
from requests import Response
import os
from typing import Optional
import logging
import dotenv
from result import Err, Ok, Result

SHOW_DEBUG = False
LASTMILE_SPAN_KIND_KEY_NAME = "lastmile.span.kind"


class Singleton:
    """
    Define a Singleton object that we can extend to create singleton classes.
    This is needed/helpful for ensuring trace-level data is the same when used
    across multiple classes. An alternative to using a singleton is ensuring
    that a shared state object is passed around correctly to all callsites

    This implementation is what's found on the Python docs:
    https://www.python.org/download/releases/2.2/descrintro/#__new__
    Please note that it is not thread-safe
    """

    def __new__(cls, *args, **kwargs):  # type: ignore[errggh *pukes*]
        it = cls.__dict__.get("__it__")  # dude
        if it is not None:
            return it
        cls.__it__ = it = object.__new__(cls)
        it.init(*args, **kwargs)  # type: ignore[im going to pretend i didnt see that *pukes*]
        return it

    def init(self, *args, **kwargs):  # type: ignore[mate]
        """
        Sets the _is_already_initialized flag to True. Use this in your
        cubslass with the following implementation

        class MySingleton(Singleton):
            _is_already_initialized = False

            def __init__(self):
                if self._is_already_initialized:
                    return
                super().__init__()
                # Other logic here to initialize singleton once
                ...
                _is_already_initialized = False
        """


def get_lastmile_api_token(lastmile_api_token: Optional[str] = None) -> str:
    """
    Helper function to get the LastMile API token. If the lastmile_api_token
    is None, then we try to get the token from the environment variables. If
    the token is still None, then we raise a ValueError.

    @param lastmile_api_token Optional(str): The LastMile API token to use.
        If None, then we try to get the token from the environment variables

    @return str: The LastMile API token to use
    """
    if lastmile_api_token is None:
        dotenv.load_dotenv()
        lastmile_api_token = os.getenv("LASTMILE_API_TOKEN")
        if lastmile_api_token is None:
            raise ValueError(
                "Cannot find `lastmile_api_token`. Please create one from the 'API Tokens' section from this website: https://lastmileai.dev/settings?page=tokens"
            )
    return lastmile_api_token


def raise_for_status(response: Response, message: str) -> None:
    """
    Raise an HTTPError exception if the response is not successful
    """
    try:
        response.raise_for_status()
    except requests.HTTPError as e:
        raise requests.HTTPError(f"{message}: {response.content}") from e


def log_for_status(
    response: Response, message: str, logger: Optional[logging.Logger] = None
) -> Result[Optional[Response], requests.HTTPError]:
    """
    Checks the status of an HTTP response and logs an error if the response is not successful.

    Args:
        response (Response): The HTTP response object to check.
        error_message (str): The error message to include in the log.

    Returns:
        Result[Optional[Response], requests.HTTPError]:
            - If the response is successful (status code in the 2xx range), returns Ok(response).
            - If the response is not successful, logs an error and returns Err(requests.HTTPError).

    Raises:
        None

    Example:
        response = requests.get("https://api.example.com/data")
        result = log_for_status(response, "Failed to fetch data")
        match result:
            case Ok(response):
                # Handle successful response
                pass
            case Err(http_error):
                # Handle the specific HTTPError exception
                pass
    """
    try:
        response.raise_for_status()
        return Ok(response)
    except requests.HTTPError as e:
        if logger:
            logger.error(
                "%s: %s - %s - %s",
                message,
                response.status_code,
                response.reason,
                response.text,
                stack_info=True,
            )  # % formatting is preferred over fstrings by logging lib
        else:
            logging.error(
                "%s: %s - %s - %s",
                message,
                response.status_code,
                response.reason,
                response.text,
                stack_info=True,
            )  # % formatting is preferred over fstrings by logging lib
        return Err(e)
