import contextvars
import typing
from functools import partial

from aiohttp import web
from werkzeug.local import LocalProxy

__version__ = '0.0.1'

ctx = contextvars.ContextVar('request')  # type: contextvars.ContextVar


class ThreadContext:

    __slots__ = ('_ctx', '_fn')

    def __init__(self, fn: typing.Callable) -> None:
        self._fn = fn

        self._ctx = contextvars.copy_context()  # type: contextvars.Context

    def __call__(self, *args, **kwargs):
        return self._ctx.run(partial(self._fn, *args, **kwargs))


def middleware_factory() -> typing.Awaitable:
    @web.middleware
    async def middleware(
        request: web.Request,
        handler: typing.Callable,
    ) -> web.Response:
        token = ctx.set(request)  # type: contextvars.Token

        try:
            return await handler(request)
        finally:
            ctx.reset(token)

    return middleware


def get_request() -> web.Request:
    return ctx.get()


grequest = LocalProxy(get_request)
