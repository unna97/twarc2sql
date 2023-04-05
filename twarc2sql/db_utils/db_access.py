"""
This should appear in the docstring for the module
"""



import pandas as pd
import numpy as np
import os
from sqlalchemy.dialects.postgresql import insert
import sqlalchemy as sa
import dotenv 
import sqlalchemy_utils as sau
import logging
from typing import Optional, Dict, List, Any
from .models import Base

logging.basicConfig(level=logging.INFO) 


class DatabaseException(Exception):
    
    def __init__(self, message:str):

        self.message = message


def create_uri(db_name:str, db_user:str, db_password:str, db_host:str, db_port:str) -> str:
    """
    Create a URI string for a database connection

    Arguments:
    ------------------
    db_name : str
        Name of the database
    
    db_user : str
        Username for the database
    
    db_password : str
        Password for the database
    
    db_host : str
        Host for the database
    
    db_port : str
        Port for the database
    
    Returns:
    ------------------
    uri : str
    """
    logging.info(f"Creating URI for {db_name} database")
    return f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"


def create_engine(uri:str) -> sa.engine.base.Engine:
    """
    Create a SQLAlchemy engine
    
    Arguments:
    ------------------
    uri : str
        URI for the database to connect to
    
    Returns:
    ------------------
    engine : sqlalchemy.engine.base.Engine


    """
    logging.info(f"Creating engine for {uri}")
    return sa.create_engine(uri, echo=True)


def load_db_config(file_path:Optional[str]=None) -> Dict[str, str]:
    """
    Load environment variables from file_path and return a dictionary of the database variables

    Arguments:
    ------------------
    file_path : str
        Path to the .env file. If None, defaults to .env in the current directory
    
    Returns:
    ------------------
    db_variables : dict

    Exceptions:
    ------------------
    AssertionError if the enviroment file specified does not exist or if the environment variables are not set
    """
    if file_path is None:
        file_path = '.env'
    
    logging.info(f"Loading environment variables from {file_path}")
    assert os.path.exists(file_path), f"{file_path} does not exist"
    load_env = dotenv.load_dotenv(file_path)
    assert load_env == True, "Failed to load environment variables"

    db_vars: List[str] = ['DB_NAME', 'DB_USER', 'DB_PASSWORD', 'DB_HOST', 'DB_PORT']
    for var in db_vars:
        assert os.getenv(var) is not None, f"{var} is not set in {file_path}"
    
    db_variables: Dict[str, str] = {var: os.getenv(var) for var in db_vars}
    logging.info("Loaded environment variables")
    return db_variables


def create_db(db_name:Optional[str]=None):
    """
    Create a database if it does not already exist with the specified name

    Arguments:
    ------------------
    db_name : str
        Name of the database to create. If None, defaults to the database specified in the environment file
    
    Returns:
    ------------------
    engine : sqlalchemy.engine.base.Engine
        SQLAlchemy engine for the database
    
    Exceptions:
    ------------------
    DatabaseException if the database already exists
    sa.exc.OperationalError if the database could not be created or connected to after creation

    """
    db_vars = load_db_config()
    logging.info(f"Creating {db_vars['DB_NAME']} database")

    if db_name is not None:
        db_vars['DB_NAME'] = db_name 
    
    uri = create_uri(db_name=db_vars['DB_NAME'], db_user=db_vars['DB_USER'], 
                     db_password=db_vars['DB_PASSWORD'], db_host=db_vars['DB_HOST'], 
                     db_port=db_vars['DB_PORT'])
    engine = create_engine(uri)
    
    if not sau.database_exists(uri):
        sau.create_database(uri)
    else:
        logging.error(f"Failed to create {db_vars['DB_NAME']} database as it already exists")
        raise DatabaseException(f"{db_vars['DB_NAME']} database already exists")
    
    try:
        connect = engine.connect()
        connect.close()
    except sa.exc.OperationalError:
        logging.error(f"Failed to connect & create {db_vars['DB_NAME']} database")
        raise sa.exc.OperationalError
    logging.info(f"Successfully created {db_vars['DB_NAME']} database")

    return engine


def delete_db(db_name:Optional[str]=None) -> bool:

    """
    Delete a database if it exists with the specified name or do nothing if it does not exist

    Arguments:
    ------------------
    db_name : str
        Name of the database to delete. If None, defaults to the database specified in the environment file
    
    Returns:
    ------------------
    db_does_not_exist : bool
        True if the database does not exist, False otherwise

     Note:- This is not a guarantee that the database was deleted. It is possible that the database was deleted
        or that the database did not exist in the first place.
    """

    db_vars:Dict[Any] = load_db_config()

    if db_name is not None:
        db_vars['DB_NAME'] = db_name 

    logging.info(f"Deleting {db_vars['DB_NAME']} database")

    uri:str = create_uri(db_name=db_vars['DB_NAME'], db_user=db_vars['DB_USER'], 
                     db_password=db_vars['DB_PASSWORD'], db_host=db_vars['DB_HOST'], db_port=db_vars['DB_PORT'])

    if sau.database_exists(uri):
        sau.drop_database(uri)
        logging.info(f"Successfully executed delete command {db_vars['DB_NAME']} database")
    else: 
        logging.warning(f"{db_vars['DB_NAME']} database does not exist")
    
    db_does_not_exist:bool = not sau.database_exists(uri)
   
    return db_does_not_exist

def create_tables(engine:sa.engine, base: Any) -> None:

    """
    Create the tables for the database

    Arguments:
    ------------------
    engine : sqlalchemy.engine.base.Engine
        SQLAlchemy engine for the database
    base : sqlalchemy.ext.declarative.api.DeclarativeMeta
        Base class for the database schema
    
    Returns:
    ------------------
    None
    """
    tables_created:List[str] = [table for table in base.metadata.tables.keys()]
    logging.info(f"Creating tables {tables_created} for database")
    base.metadata.create_all(engine)
    logging.info("Successfully created tables for database")

def create_db_with_tables(db_name:Optional[str]=None):
    """
    Create a database and create the tables for the database

    Arguments:
    ------------------
    None
    
    Returns:
    ------------------
    engine : sqlalchemy.engine.base.Engine
        SQLAlchemy engine for the database
    """
    if db_name is None:
        db_name = load_db_config()['DB_NAME']
    
    logging.info(f"Creating database {db_name} and tables")

    engine = create_db(db_name=db_name)
    
    create_tables(engine, Base)
    return engine


