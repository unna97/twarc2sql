"""Functions to process objects from the twitter API and convert them to tables."""
from typing import Dict, List, Optional

import pandas as pd

from . import object_columns, table_columns


def expand_dict_column(
    data: pd.DataFrame, column: str, keys: Optional[List] = None
) -> pd.DataFrame:
    """
    expand_dict_column expands a dict column.

    This function converts a column that contains a dictionary
    into multiple columns. The keys of the dictionary are used.

    Parameters
    ----------
    data : pd.DataFrame
        the data to expand
    column : str
        the column to expand
    keys : Optional[List]
        the keys to expand. If None, the keys are taken from
        the first row of the column.

    Returns
    -------
    data : pd.DataFrame
        the data with the expanded column

    """
    if keys is None:
        keys = data[column].dropna().iloc[0].keys()

    for key in keys:
        data[key] = data[column].apply(lambda x: x.get(key))
    return data


# TODO: Replace this with great expectations validation?
def validate_object(object: pd.DataFrame, object_type: str):
    """
    validate_object validates objects in format of the twitter API.

    It validates that the object has the correct columns and
    that it has at least one row.

    Parameters
    ----------
    object : pd.DataFrame
        the object to validate
    object_type : str
        the type of object to validate (tweet_object, user_object)

    Raises
    ------
    AssertionError
        if the object does not have the correct columns or has no rows
    """
    assert (
        object_type in object_columns.keys()
    ), f"Object type must be one of {object_columns.keys()}"
    assert object.shape[0] > 0, f"{object_type} must have at least one row"
    assert set(object.columns) == set(
        object_columns[object_type]
    ), f"{object_type} columns must be {object_columns[object_type]}"


def refrenced_tweet_column_processing(
    tweet_object: pd.DataFrame, tables: Dict[str, List[pd.DataFrame]]
):
    """
    refrenced_tweet_column_processing.

    Parameters
    ----------
    tweet_object : pd.DataFrame
        The raw tweet object to be processed
    tables : Dict[str, List[pd.DataFrame]]
       The tables to upload to the database

    Returns
    -------
    tables : Dict[str, List[pd.DataFrame]]
         The tables to upload to the database with the refrenced tweets added
    """
    columns = ["id", "in_reply_to_user_id", "referenced_tweets"]
    referenced_tweets = tweet_object[columns]
    referenced_tweets = referenced_tweets.explode("referenced_tweets")
    referenced_tweets.dropna(subset=["referenced_tweets"], inplace=True)
    referenced_tweets.reset_index(drop=True, inplace=True)

    referenced_tweets.rename({"id": "actual_id"}, axis=1, inplace=True)

    expand_dict_column(referenced_tweets, "referenced_tweets", ["id", "type"])

    referenced_tweets.rename(
        {"id": "tweet_id", "actual_id": "id"}, axis=1, inplace=True
    )

    # TODO: fetch below from init
    columns_for_each = {
        "quoted": ["tweet_id", "id"],
        "retweeted": ["tweet_id", "id"],
        "replied_to": [
            "tweet_id",
            "id",
            "in_reply_to_user_id",
        ],
    }

    for key, columns_for_table in columns_for_each.items():
        table_name = key + "_tweet_mapping"
        tables[table_name].append(
            referenced_tweets[referenced_tweets["type"] == key][columns_for_table]
        )

    return tables


def tweet_object_to_table(
    tweet_object: pd.DataFrame, tables: Dict[str, pd.DataFrame]
) -> Dict[str, pd.DataFrame]:
    """
    Process a tweet object and add it to the tables.

    The columns public_metrics and edit_controls are expanded into their own columns.

    Parameters
    ----------
    tweet_object : pd.DataFrame
        the tweet object from chunk
    tables : Dict[str, pd.DataFrame]
        all tables that have been created
    Returns
    -------
    tables : Dict[str, pd.DataFrame]
        tables that have been updated with the tweet_object
    """
    # validate_object(tweet_object, "tweet_object")

    refrenced_tweet_column_processing(tweet_object, tables)

    tweet_object = expand_dict_column(tweet_object, "public_metrics")
    tweet_object = expand_dict_column(tweet_object, "edit_controls")

    # TODO: Add processing for referenced tweets and assign tweet_type
    tweet_object["tweet_type"] = 0

    columns_for_tweet_table = table_columns["tweet"]
    tables["tweet"].append(tweet_object[columns_for_tweet_table])

    return tables


def user_object_to_table(user_object: pd.DataFrame, tables: Dict[str, pd.DataFrame]):
    """
    Process a user object and add it to the tables.

    Parameters
    ----------
    user_object : pd.DataFrame
        the user object from chunk
    tables : Dict[str, pd.DataFrame]
        all tables that have been created
    Returns
    -------
    tables : Dict[str, pd.DataFrame]
        tables that have been updated with the user_object
    """
    # validate_object(user_object, "user_object")

    user_object = expand_dict_column(user_object, "public_metrics")

    columns_for_user_table = table_columns["author"]
    tables["author"].append(user_object[columns_for_user_table])

    return tables
