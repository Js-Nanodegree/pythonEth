import asyncio

import aiohttp
import async_timeout


async def fetch(session, params, timeout=60):
    with async_timeout.timeout(timeout):
        try:
            async with session.request(**params) as resp:
                if resp.status == 200:
                    answer = await resp.json()
                    responce = (resp.status, resp.reason, answer)
                else:
                    responce = (resp.status, resp.reason, None)
                return responce
        except:
            raise


async def send_request_aiohttp(params):
    loop = asyncio.get_running_loop()
    async with aiohttp.ClientSession(loop=loop) as session:
        try:
            answer = await fetch(session, params)
        except Exception as msg:
            return (None, 'Fall Fetching', str(msg))
        return answer
