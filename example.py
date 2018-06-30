import asyncio

from aiohttp import web
from aiohttp_request import ThreadContext, middleware_factory, grequest, get_request


def thread():
    assert grequest['sense'] == 42


async def task():
    # grequest is `lazy` version of request
    assert grequest['sense'] == 42

    # works for threads as well with ThreadContext
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, ThreadContext(thread))


async def hello(request):
    # get_request is on-demand function to get current request
    assert get_request() is request

    request['sense'] = 42

    await asyncio.ensure_future(task())

    return web.Response(text="Hello, world")


app = web.Application(middlewares=[middleware_factory()])
app.add_routes([web.get('/', hello)])
web.run_app(app)
