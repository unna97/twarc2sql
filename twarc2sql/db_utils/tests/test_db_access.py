"""
Tests for the db_access module.

The tests are run using pytest. To run the tests, use the following command from the 
root directory of the project:

    pytest twarc2sql/db_utils/tests/test_db_access.py

"""


import os
from typing import Dict

import pandas as pd
import pytest
import sqlalchemy as sa
import sqlalchemy_utils as sau

from twarc2sql.db_utils import db_access


def test_create_uri(uri):
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
        "DB_USER": "random_user",
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


def test_create_engine(config_file_path, uri):
    """
    Test that the create_engine function returns an engine.

    The engine should be a sqlalchemy.engine.base.Engine object.
    """
    engine = db_access.create_engine(uri)
    assert isinstance(engine, sa.engine.base.Engine)
    engine.dispose()


def test_delete_db(config_file_path):
    """
    Test that the delete_db function returns True.

    The function should return True if the database is deleted.
    """
    assert db_access.delete_db(config_file_path)


def test_create_db(config_file_path):
    """
    Test that the create_engine function returns an engine.

    The engine should be a sqlalchemy.engine.base.Engine object.
    """
    engine = db_access.create_db(config_file_path)
    assert sau.database_exists(engine.url)
    # check that the database exists without tables:
    assert isinstance(engine, sa.engine.base.Engine)
    with pytest.raises(db_access.DatabaseException, match="database already exists"):
        db_access.create_db(config_file_path)
    # make sure that the database is deleted:
    assert db_access.delete_db(config_file_path)
    # check that the database does not exist:
    engine.dispose()


def test_get_engine(config_file_path):
    """
    Test that the get_engine function returns an engine.

    The engine should be a sqlalchemy.engine.base.Engine object.
    """
    with pytest.raises(db_access.DatabaseException, match="database does not exist"):
        engine = db_access.get_engine(config_file_path)
    # create the database:
    engine = db_access.create_db(config_file_path)
    assert sau.database_exists(engine.url)
    engine = db_access.get_engine(config_file_path)
    # check that the database exists without tables:
    assert isinstance(engine, sa.engine.base.Engine)
    # make sure that the database is deleted:
    assert db_access.delete_db(config_file_path)
    # check that the database does not exist:
    engine.dispose()


def test_create_tables(engine, base_tables, tables_and_columns):
    """
    Test that the create_tables function returns True.

    The function should return True if the tables are created.
    """
    # create the tables:
    db_access.create_tables(engine=engine, base=base_tables)
    # check that the tables exist:
    assert sau.database_exists(engine.url)
    # Use pandas to check that the tables exist:
    conn = engine.connect()

    for table in tables_and_columns.keys():
        df = pd.read_sql_table(table, conn)
        assert set(df.columns.tolist()) == set(tables_and_columns[table])
        assert df.empty
    conn.close()


def test_create_db_with_tables(config_file_path, tables_and_columns):
    """
    Test that the create_db_with_tables function returns an engine.

    The engine should be a sqlalchemy.engine.base.Engine object.
    """
    assert db_access.delete_db(config_file_path)
    engine = db_access.create_db_with_tables(config_file_path)
    assert sau.database_exists(engine.url)
    # check that the tables exist:
    assert isinstance(engine, sa.engine.base.Engine)
    # Use pandas to check that the tables exist:
    conn = engine.connect()

    for table in tables_and_columns.keys():
        df = pd.read_sql_table(table, conn)
        assert set(df.columns.tolist()) == set(tables_and_columns[table])
        assert df.empty
    conn.close()
