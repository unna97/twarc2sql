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
        """
        Exception for database errors

        Parameters
        ----------
        message : str
            The error message
        
        Attributes
        ----------
        message : str
            The error message
        """

        self.message = message


def create_uri(db_name:str, db_user:str, db_password:str, db_host:str, db_port:str) -> str:
    """
    Create a URI for a database connection using the specified parameters
    
    Parameters
    ----------
    db_name : str
        the name of the database to connect to or create
    db_user : str
       the username for authentication to connect to the database
    db_password : str
        the password for authentication to connect to the database
    db_host : str
        the host of the database to connect to
    db_port : str
        the port of the database to connect to

    Returns
    -------
    uri: str
        the URI for the database
    """
    logging.info(f"Creating URI for {db_name} database")
    uri = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    return uri

 
def create_engine(uri:str) -> sa.engine.base.Engine:
    """
    Create a SQLAlchemy engine for the database specified by the URI

    Parameters
    ----------
    uri : str
        URI for the database to connect to or create

    Returns
    -------
    engine: sa.engine.base.Engine
        SQLAlchemy engine for the database
    """
    #TODO: Stop displaying the password in the logs & maybe allow users to specify echo
    logging.info(f"Creating engine for {uri}")   
    engine = sa.create_engine(uri, echo=True)
    logging.info(f"Engine created successfully for database {uri}")
    return engine

def load_db_config(file_path:Optional[str]=None) -> Dict[str, str]:
    """
    Load environment variables from file_path and return a dictionary of the database variables

    Parameters
    ----------
    file_path : Optional[str], optional
        Path to the .env file. If None, defaults to .env in the current directory, by default None

    Returns
    -------
    db_variables : Dict[str, str]
        Dictionary of the database variables
    
    Raises
    ------
    AssertionError : 
        if the environment file specified does not exist 
        or if the environment variables are not set
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


def create_db(db_name:Optional[str]=None) -> sa.engine.base.Engine:
    """
    Create a database if it does not already exist with the specified name

    Parameters
    ----------
    db_name : Optional[str], optional
        Name of the database to create if None it defaults to database enviroment file, by default None

    Returns
    -------
    engine : sa.engine.base.Engine
        SQLAlchemy engine for the database created

    Raises
    ------
    DatabaseException
        if the database already exists
    sa.exc.OperationalError
        if the database could not be created
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

#TODO: Throw an exception if the database does not exist?
def delete_db(db_name:Optional[str]=None) -> bool:
    """
    Delete a database if it exists with the specified name or do nothing if it does not exist

    Note
    ----
    This is not a guarantee that the database was deleted. The database may not exist in the first place.

    Parameters
    ----------
    db_name : Optional[str], optional
         Name of the database to delete. If None, defaults to the database specified in the environment file, by default None

    Returns
    -------
    db_does_not_exist : bool
        True if the database does not exist, False otherwise
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

    Parameters
    ----------
    engine : sa.engine
        SQLAlchemy engine for the database

    base : sqlalchemy.ext.declarative.api.DeclarativeMeta
        Base class for the database schema
    
    Returns
    -------
    None
    """
    tables_created:List[str] = [table for table in base.metadata.tables.keys()]
    logging.info(f"Creating tables {tables_created} for database")
    base.metadata.create_all(engine)
    logging.info("Successfully created tables for database")

def create_db_with_tables(db_name:Optional[str]=None):
    """
    Create a database and create the tables for the database

    This is a wrapper function for create_db and create_tables functions

    Parameters
    ----------
    db_name : Optional[str], optional
        Name of the db created, by default None

    Returns
    -------
    engine : sa.engine.base.Engine
        SQLAlchemy engine for the database created
    """
    
    if db_name is None:
        db_name = load_db_config()['DB_NAME']
    
    logging.info(f"Creating database {db_name} and tables")

    engine = create_db(db_name=db_name)
    
    create_tables(engine, Base)
    return engine


