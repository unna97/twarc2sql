"""
Tests for the db_access module.

The tests are run using pytest. To run the tests, use the following command from the 
root directory of the project:

    pytest twarc2sql/db_utils/tests/test_db_access.py

"""


import os
from typing import Dict

import pytest

from twarc2sql.db_utils import db_access


def test_create_uri():
    """
    Test that the create_uri function returns the correct URI.

    The URI should be in the format: postgresql://user:password@host:port/db_name
    """
    assert (
        db_access.create_uri(
            "test_db", "test_user", "test_password", "test_host", "test_port"
        )
        == "postgresql://test_user:test_password@test_host:test_port/test_db"
    )


def test_load_db_config():
    """
    Test that the load_db_config function returns a dictionary.

    The dictionary should contain the correct keys and values.
    """
    config: Dict[str, str] = {
        "DB_NAME": "test_db",
        "DB_USER": "postgres",
        "DB_PASSWORD": "postgres",
        "DB_HOST": "localhost",
        "DB_PORT": "5432",
    }
    test_env_path = "tests/data/.testenv"
    assert os.path.exists(test_env_path)
    assert isinstance(db_access.load_db_config(test_env_path), dict)

    assert db_access.load_db_config(test_env_path) == config


def test_load_db_config_missing_file():
    """
    Test that the load_db_config function raises an error for following cases.

        - file_path does not exist.

    """
    with pytest.raises(AssertionError):
        db_access.load_db_config("tests/data/.env2")

    # TODO:remove optional allowance of file_path = None
    # with pytest.raises(AssertionError):
    #     db_access.load_db_config()
