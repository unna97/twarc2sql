"""file_to_object.py convert a file to objects to be processed.

This module contains functions to convert a file to objects to 
be processed for each endpoint.
"""

from typing import Any, Dict, List

import pandas as pd


def add_meta_info(x: Dict[str, Any], twarc_meta: Dict[str, Any]) -> pd.DataFrame:
    """
    add_meta_info is converts dict to df and adds meta information.

    a function that takes a dictionary of data and a dictionary of meta information
    and returns a dataframe with the meta information added to the data.

    Parameters
    ----------
    x : Dict[str, Any]
        The dictionary of data
    twarc_meta : Dict[str, Any]
        The dictionary of meta information
    """
    x = pd.DataFrame(x)
    for key in twarc_meta:
        x["twarc_meta_" + key] = twarc_meta[key]
    return x


def get_object_for_search(
    chunk: pd.DataFrame, objects: Dict[str, List[pd.DataFrame]]
) -> Dict[str, List[pd.DataFrame]]:
    """
    get_object_for_search converts df to objects.

    The function takes a chunk of a dataframe and returns a dictionary of
    objects to be processed for the search endpoint.

    The potential objects are:
    - tweets_object
    - users_object
    - media_object
    - places_object
    - polls_object
    - error_info_object

    Parameters
    ----------
    chunk : pd.DataFrame
        The chunk of the dataframe to be processed
    objects : Dict[str, List[pd.DataFrame]]
        The dictionary of objects to be returned

    Returns
    -------
    objects : Dict[str, List[pd.DataFrame]]
        The dictionary of objects with the new objects added
    """
    objects["tweets_object"] += chunk.apply(
        lambda x: add_meta_info(x["data"], x["__twarc"]), axis=1
    ).tolist()
    includes = ["users", "tweets", "media", "places", "polls"]
    for include in includes:
        objects[f"{include}_object"] += chunk.apply(
            lambda x: add_meta_info(x["includes"].get(include), x["__twarc"]), axis=1
        ).tolist()

    objects["error_info_object"] += (
        chunk.dropna(subset=["errors"])
        .apply(lambda x: add_meta_info(x["errors"], x["__twarc"]), axis=1)
        .tolist()
    )
    objects["meta_object"] += chunk["__twarc"].tolist()
    return objects
