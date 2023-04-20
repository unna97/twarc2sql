"""Contains fixtures for tests for the db_utils module."""

import pytest
import sqlalchemy as sa

from twarc2sql.db_utils import db_access


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


@pytest.fixture(scope="module")
def uri(config_file_path):
    """
    uri _summary_.

    returns a URI
    """
    config = db_access.load_db_config(config_file_path)
    return "postgresql://{}:{}@{}:{}/{}".format(
        config["DB_USER"],
        config["DB_PASSWORD"],
        config["DB_HOST"],
        config["DB_PORT"],
        config["DB_NAME"],
    )


# create a fixture that returns a engine:
@pytest.fixture(scope="module")
def engine(config_file_path) -> sa.engine.base.Engine:
    """
    engine _summary_.

    returns a sqlalchemy engine

    Parameters
    ----------
    config_file_path : str
        path to a .env file

    Returns
    -------
    sa.engine.base.Engine
        sqlalchemy engine
    """
    db_access.delete_db(config_file_path)
    engine = db_access.create_db(config_file_path)
    yield engine
    engine.dispose()
    db_access.delete_db(config_file_path)


@pytest.fixture(scope="module")
def base_tables():
    """base_tables."""
    from twarc2sql.db_utils.models import Base

    return Base


# create a fixture that returns a tables & columns dict:
@pytest.fixture(scope="module")
def tables_and_columns() -> dict:
    """
    tables_and_columns _summary_.

    returns a dict of tables and columns

    Returns
    -------
    dict
        dict of tables and columns
    """
    # TODO: add more tables and columns
    table_columns = {
        "tweet": [
            "id",
            "created_at",
            "text",
            "possibly_sensitive",
            "conversation_id",
            "author_id",
            "reply_settings",
            "lang",
            "in_reply_to_user_id",
            "tweet_type",
            "retweet_count",
            "reply_count",
            "like_count",
            "quote_count",
            "impression_count",
            "edits_remaining",
            "is_edit_eligible",
            "editable_until",
        ],
        "author": [
            "id",
            "name",
            "username",
            "created_at",
            "description",
            "location",
            "verified",
            "protected",
            "url",
            "profile_image_url",
            "followers_count",
            "following_count",
            "tweet_count",
            "listed_count",
        ],
    }
    return table_columns
