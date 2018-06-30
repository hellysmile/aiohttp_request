import asyncio
import time

import pytest

from aiohttp_request import ThreadContext, get_request, grequest

pytestmark = pytest.mark.asyncio


async def test_basic(test_case):

    async def side_efect():
        grequest['text'] = 'basic'

    response = await test_case(side_efect)

    assert response == 'basic'


async def test_task(test_case):
    async def task():
        grequest['text'] = 'task'

    async def side_efect():
        await asyncio.ensure_future(task())

    response = await test_case(side_efect)

    assert response == 'task'


async def test_task_background(test_case):
    request = None

    async def task():
        await asyncio.sleep(0.1)
        grequest['background_done'] = True

    async def side_efect():
        nonlocal request

        asyncio.ensure_future(task())

        request = get_request()

        request['text'] = 'background'
        request['background_done'] = False

    response = await test_case(side_efect)

    assert response == 'background'

    await asyncio.sleep(0.2)

    assert request['background_done']


async def test_task_thread(test_case, loop):
    def task():
        grequest['text'] = 'thread'

    async def side_efect():
        await loop.run_in_executor(None, ThreadContext(task))

    response = await test_case(side_efect)

    assert response == 'thread'


async def test_thread_background(test_case, loop):
    request = None

    def _task():
        time.sleep(0.1)
        grequest['thread_done'] = True

    async def task():
        await loop.run_in_executor(None, ThreadContext(_task))

    async def side_efect():
        nonlocal request

        asyncio.ensure_future(task())

        request = get_request()

        request['text'] = 'thread'
        request['thread_done'] = False

    response = await test_case(side_efect)

    assert response == 'thread'

    await asyncio.sleep(0.2)

    assert request['thread_done']
