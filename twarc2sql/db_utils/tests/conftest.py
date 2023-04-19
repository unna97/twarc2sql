"""Contains fixtures for tests for the db_utils module."""

import pytest


# create a fixture that returns a engine:
@pytest.fixture(scope="module")
def config_file_path() -> str:
    """
    config_file_path _summary_.

    returns a path to a .env file

    Returns
    -------
    str
        path to a .env file
    """
    return "tests/data/.testenv"
