#!/usr/bin/env python
"""Tests for `synthientpy` package."""

import asyncio

# pylint: disable=redefined-outer-name
import os

from dotenv import load_dotenv

import synthientpy as synthient

load_dotenv()


# https://stackoverflow.com/questions/23033939/how-to-test-python-3-4-asyncio-code
def async_test(coro):
    def wrapper(*args, **kwargs):
        loop = asyncio.new_event_loop()
        try:
            return loop.run_until_complete(coro(*args, **kwargs))
        finally:
            loop.close()

    return wrapper


def test_sync_lookup():
    client = synthient.Client(
        api_key=os.getenv("SYNTHIENT_API_KEY"),
    )
    response = client.lookup("b80fd0f58c61053c3d95f01c6dc94141")
    assert response.token == "b80fd0f58c61053c3d95f01c6dc94141"


@async_test
async def test_async_lookup():
    client = synthient.AsyncClient(
        api_key=os.getenv("SYNTHIENT_API_KEY"),
    )
    response = await client.lookup("b80fd0f58c61053c3d95f01c6dc94141")

    assert response.token == "b80fd0f58c61053c3d95f01c6dc94141"


def test_sync_404():
    client = synthient.Client(
        api_key=os.getenv("SYNTHIENT_API_KEY"),
    )
    try:
        client.lookup("NONEXISTENT_TOKEN")
    except synthient.ErrorResponse as e:
        assert e.message == "Visitor not found"


@async_test
async def test_async_404():
    client = synthient.AsyncClient(
        api_key=os.getenv("SYNTHIENT_API_KEY"),
    )
    try:
        await client.lookup("NONEXISTENT_TOKEN")
    except synthient.ErrorResponse as e:
        assert e.message == "Visitor not found"


def test_sync_401():
    client = synthient.Client(
        api_key="INVALID_API_KEY",
    )
    try:
        client.lookup("b80fd0f58c61053c3d95f01c6dc94141")
    except synthient.ErrorResponse as e:
        assert e.message == "Unauthorized"


@async_test
async def test_async_401():
    client = synthient.AsyncClient(
        api_key="INVALID_API_KEY",
    )
    try:
        await client.lookup("b80fd0f58c61053c3d95f01c6dc94141")
    except synthient.ErrorResponse as e:
        assert e.message == "Unauthorized"


def test_sync_visits():
    client = synthient.Client(
        api_key=os.getenv("SYNTHIENT_API_KEY"),
    )
    response = client.visits("6067acf071d3285097b65abc451c2192")
    assert len(response.visits) == 7 and not response.has_next


@async_test
async def test_async_visits():
    client = synthient.AsyncClient(
        api_key=os.getenv("SYNTHIENT_API_KEY"),
    )
    response = await client.visits("6067acf071d3285097b65abc451c2192")

    assert len(response.visits) == 7 and not response.has_next


def test_verify():
    client = synthient.Client(
        api_key=os.getenv("SYNTHIENT_API_KEY"),
    )
    response = client.lookup("b80fd0f58c61053c3d95f01c6dc94141")
    response.consumed = False  # just for tests
    assert synthient.verify_token(response, synthient.models.TokenType.SIGN) is True


@async_test
async def test_verify():
    client = synthient.AsyncClient(
        api_key=os.getenv("SYNTHIENT_API_KEY"),
    )
    response = await client.lookup("b80fd0f58c61053c3d95f01c6dc94141")
    response.consumed = False  # just for tests
    assert synthient.verify_token(response, synthient.models.TokenType.SIGN) is True
