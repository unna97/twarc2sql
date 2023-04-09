#!/usr/bin/env python

"""Tests for `twarc2sql` package."""


import pandas as pd
import pytest


@pytest.fixture
def response():
    """Sample pytest fixture.

    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    # import requests
    # return requests.get('https://github.com/audreyr/cookiecutter-pypackage')
    # read the jsonl file and return the first line:
    tweets = pd.read_json("./tests/data/example.jsonl", lines=True)
    return tweets


def test_content(response):
    """Sample pytest test function with the pytest fixture as an argument."""
    # from bs4 import BeautifulSoup
    # assert 'GitHub' in BeautifulSoup(response.content).title.string
    print(type(response))
    assert type(response) == pd.core.frame.DataFrame


def test_example():
    """Sample pytest test function with twarc2sql code."""
    from twarc2sql.db_utils import db_access

    assert (
        db_access.create_uri("test", "test", "test", "test", "test")
        == "postgresql://test:test@test:test/test"
    )
