# ruff: noqa: S101
import json
import os
import pathlib
from io import BytesIO

import httpx
import pytest

pytest_plugins = ("pytest_asyncio",)


@pytest.mark.asyncio
async def test_fastapi_endpoint_get_string():
    async with httpx.AsyncClient() as client:
        r = await client.get("http://localhost:8000/get-string", headers={"Content-Type": "application/json"})
    assert r.status_code == 200
    assert r.text == "return a string"


@pytest.mark.asyncio
async def test_fastapi_endpoint_get_json():
    async with httpx.AsyncClient() as client:
        r = await client.get("http://localhost:8000/get-json", headers={"Content-Type": "application/json"})
    assert r.status_code == 200
    assert r.json() == {"json_obj": "return json"}


@pytest.mark.asyncio
async def test_fastapi_endpoint_parameter_found():
    async with httpx.AsyncClient() as client:
        r = await client.get(
            "http://localhost:8000/get-not-found-parameter/found", headers={"Content-Type": "application/json"}
        )
    assert r.status_code == 200
    assert r.json() == {"status": "item found"}


@pytest.mark.asyncio
async def test_fastapi_endpoint_parameter_not_found():
    async with httpx.AsyncClient() as client:
        r = await client.get(
            "http://localhost:8000/get-not-found-parameter/not", headers={"Content-Type": "application/json"}
        )
    assert r.status_code == 204


@pytest.mark.asyncio
async def test_fastapi_endpoint_payload():
    async with httpx.AsyncClient() as client:
        r = await client.post(
            "http://localhost:8000/post-payload",
            headers={"Content-Type": "application/json"},
            content=json.dumps({"name": "Ben", "age": 20}),
        )
    assert r.status_code == 200
    assert r.json() == {"name": "Ben", "age": 20}


@pytest.mark.asyncio
async def test_fastapi_endpoint_download_text_file():
    async with httpx.AsyncClient() as client:
        r = await client.get("http://localhost:8000/get-text-download", headers={"Content-Type": "application/json"})
    assert r.status_code == 200
    buffer = BytesIO(r.content)
    assert buffer.getvalue().decode() == "name,age,weight\nben,40,154\nsam,32,185"


@pytest.mark.asyncio
async def test_fastapi_endpoint_download_image_file():
    async with httpx.AsyncClient() as client:
        r = await client.get("http://localhost:8000/get-image-download", headers={"Content-Type": "application/json"})
    assert r.status_code == 200
    with open("test.jpg", "wb") as f:
        f.write(r.content)
    assert os.path.isfile("test.jpg")
    assert os.path.getsize("test.jpg") == 338148
    # clean up
    if os.path.isfile("test.jpg"):
        pathlib.Path("test.jpg").unlink()
    assert os.path.isfile("test.jpg") is False


@pytest.mark.asyncio
async def test_fastapi_endpoint_streaming():
    streamed_l = []
    async with httpx.AsyncClient() as client:
        async with client.stream(
            "GET", "http://localhost:8000/get-streaming", headers={"Content-Type": "application/json"}
        ) as r:
            async for chunk in r.aiter_lines():
                streamed_l.append(chunk)
    assert r.status_code == 200
    for count, i in enumerate(streamed_l):
        i = json.loads(i)
        assert count == i["event"]
        if count == 39:
            assert i["is_last_event"] is True
        else:
            assert i["is_last_event"] is False
