import asyncio

from aiohttp import web
from aiohttp_request import middleware_factory, grequest
from contextvars_executor import ContextVarExecutor


def thread():
    assert grequest['sense'] == 42


async def hello(request):
    request['sense'] = 42

    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, thread)

    return web.Response(text="Hello, world")


loop = asyncio.get_event_loop()
loop.set_default_executor(ContextVarExecutor())
app = web.Application(middlewares=[middleware_factory()])
app.add_routes([web.get('/', hello)])
web.run_app(app)
