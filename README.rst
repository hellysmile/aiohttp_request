aiohttp_request
===============

:info: Global request for aiohttp server

.. image:: https://travis-ci.org/hellysmile/aiohttp_request.svg?branch=master
    :target: https://travis-ci.org/hellysmile/aiohttp_request

.. image:: https://img.shields.io/pypi/v/aiohttp_request.svg
    :target: https://pypi.python.org/pypi/aiohttp_request

.. image:: https://codecov.io/gh/hellysmile/aiohttp_request/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/hellysmile/aiohttp_request

Installation
------------

.. code-block:: shell

    pip install aiohttp_request

Usage
-----

.. code-block:: python

    import asyncio

    from aiohttp import web
    from aiohttp_request import ThreadContext, middleware_factory, grequest, get_request


    def thread():
        assert grequest['sense'] == 42


    async def task():
        # grequest is `lazy` version of request
        assert grequest['sense'] == 42

        loop = asyncio.get_event_loop()
        # works for threads as well with ThreadContext
        await loop.run_in_executor(None, ThreadContext(thread))


    async def hello(request):
        # get_request is on-demand function to get current request
        assert get_request() is request

        request['sense'] = 42

        # asyncio.Task is supported
        await asyncio.ensure_future(task())

        return web.Response(text="Hello, world")


    app = web.Application(middlewares=[middleware_factory()])
    app.add_routes([web.get('/', hello)])
    web.run_app(app)

Python 3.7+ is required, there is no way to support older python versions!!!

Notes
-----

The library relies on `PEP 567 <https://www.python.org/dev/peps/pep-0567/>`_ and its `asyncio support <https://docs.python.org/3.7/library/contextvars.html#asyncio-support>`_

aiohttp-request works nicely with threads via `contextvars_executor <https://github.com/hellysmile/contextvars_executor>`_ , no `ThreadContext` is needed

.. code-block:: python

    import asyncio

    from aiohttp import web
    from aiohttp_request import middleware_factory, grequest
    from contextvars_executor import ContextVarExecutor


    def thread():
        assert grequest['sense'] == 42


    async def hello(request):
        request['sense'] = 42

        await loop.run_in_executor(None, thread)

        return web.Response(text="Hello, world")


    loop = asyncio.get_event_loop()
    loop.set_default_executor(ContextVarExecutor())
    app = web.Application(middlewares=[middleware_factory()])
    app.add_routes([web.get('/', hello)])
    web.run_app(app)
