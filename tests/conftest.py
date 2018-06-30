import asyncio
import gc
import os

import pytest
from aiohttp import web
from aiohttp.test_utils import TestClient, TestServer

from aiohttp_request import middleware_factory

asyncio.set_event_loop(None)  # type: ignore


@pytest.fixture
def event_loop(request):
    loop = asyncio.new_event_loop()
    loop.set_debug(bool(os.environ.get('PYTHONASYNCIODEBUG')))

    yield loop

    loop.run_until_complete(loop.shutdown_asyncgens())

    loop.call_soon(loop.stop)
    loop.run_forever()
    loop.close()

    gc.collect()
    gc.collect()  # for pypy


@pytest.fixture
def loop(event_loop, request):
    asyncio.set_event_loop(None)
    request.addfinalizer(lambda: asyncio.set_event_loop(None))  # type: ignore

    return event_loop


@pytest.fixture
def aiohttp_client(loop):
    clients = []

    async def go(app):
        server = TestServer(app, loop=loop)
        client = TestClient(server, loop=loop)

        await client.start_server()

        clients.append(client)

        return client

    yield go

    async def finalize():
        while clients:
            await clients.pop().close()

    loop.run_until_complete(finalize())


@pytest.fixture
def test_case(aiohttp_client):

    async def go(side_effect):
        async def hello(request):
            await side_effect()

            return web.Response(text=request['text'])

        app = web.Application(middlewares=[middleware_factory()])
        app.router.add_get('/', hello)

        client = await aiohttp_client(app)

        response = await client.get('/')

        assert response.status == 200

        text = await response.text()

        return text

    yield go
