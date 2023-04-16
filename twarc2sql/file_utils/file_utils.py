"""file_utils contains functions to read files and upload them to the database."""

from typing import Any, Dict

import pandas as pd
from sqlalchemy.dialects.postgresql import insert

from twarc2sql.db_utils.db_access import create_db_with_tables, get_engine

from . import objects
from .file_to_object import get_object_for_search
from .object_to_table import tweet_object, user_object

table_priority = ["meta", "author", "tweet", "media", "places", "polls", "errors"]


def upload_to_database(tables: Dict[str, pd.DataFrame], engine: Any) -> None:
    """
    upload_to_database uploads the tables to the database.

    Parameters
    ----------
    tables : Dict[str, pd.DataFrame]
        the tables to upload to the database

    engine : Any
        the engine to connect to the database
    """
    for table in table_priority:
        current_table = tables[table]
        if len(current_table) > 0:
            current_table = pd.concat(current_table)
            print(f"Uploading {len(current_table)} rows to {table}")

            current_table.to_sql(
                table,
                engine,
                if_exists="append",
                index=False,
                method=on_duplicate_do_nothing,
            )


def read_and_upload_file(
    folder_path: str,
    file_name: str,
    task_type: str = "search",
    engine: Any = None,
    objects: Dict[str, Any] = {},
) -> Dict[str, Any]:
    """
    read_and_upload_file reads the file and uploads it to the database.

    Parameters
    ----------
    folder_path : str
        the folder path where the file is located

    file_name : str
        the name of the file

    task_type : str, optional
        the type of task that was run, by default "search"

    engine : Any, optional
        the engine to connect to the database, by default None

    objects : Dict[str, Any], optional
        the objects to upload to the database, by default {}

    Returns
    -------
    Dict[str, Any]
        the objects to uploaded to the database

    """
    # read the file in chunks:
    file_path: str = folder_path + file_name
    chunks = pd.read_json(file_path, lines=True, chunksize=1000)

    task_types = {"search": get_object_for_search}
    # create empty tables:
    tables = {table: [] for table in table_priority}

    for chunk in chunks:
        # get objects from chunk:
        objects = task_types[task_type](chunk, objects)
        # TODO:Object processing is task specific i.e diff for tasks
        # convert objects to tables:
        tables = tweet_object(pd.concat(objects["tweets_object"]), tables)
        tables = user_object(pd.concat(objects["users_object"]), tables)
        # upload tables to database:
        upload_to_database(tables, engine)
    return tables


# TODO: this function should be moved to the db_utils folder
def on_duplicate_do_nothing(table, conn, keys, data_iter) -> None:
    """on_duplicate_do_nothing uploads data to the database without duplicates.

    This function is used to upload data to the database when it encounters duplicates
    it does not upload the data & does not throw an error.

    Parameters
    ----------
    table : Any
        the table to upload the data to

    conn : Any
        the connection to the database

    keys : Any
        the keys to use to check for duplicates

    data_iter : Any
        the data to upload to the database

    """
    insert_stmt = insert(table.table).values(list(data_iter))
    on_duplicate_key_stmt = insert_stmt.on_conflict_do_nothing()
    conn.execute(on_duplicate_key_stmt)


def connect_to_db_and_upload(
    folder_path: str,
    file_name: str,
    task_type: str = "search",
    config_file_path: str = None,
) -> None:
    """
    connect_to_db_and_upload connects to the db and uploads the file to the db.

    Parameters
    ----------
    folder_path : str
        the folder path where the file is located
    file_name : str
        the name of the file
    task_type : str, optional
        the type of task that was run, by default "search"
    """
    try:
        engine = get_engine(config_file_path)
    # catch exception if database does not exist:
    except Exception as e:
        print(e)
        print("Creating database")
        engine = create_db_with_tables(config_file_path)
    tables = read_and_upload_file(folder_path, file_name, task_type, engine, objects)
    return tables
