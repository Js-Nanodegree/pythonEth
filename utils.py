import json
from web3 import Web3
import  asyncio
import aiohttp
import async_timeout


async def fetch(session, params, timeout=60):
    with async_timeout.timeout(timeout):
        try:
            async with session.request(**params) as resp:
                responce = []
                if resp.status == 200:
                    answer = await resp.json()
                    responce = [resp.reason, resp.status, answer]
                else:
                    responce = [resp.reason, resp.status, None]
                return responce
        except Exception as msg:
            raise


async def send_request_aiohttp(params):
    loop = asyncio.get_running_loop()
    async with aiohttp.ClientSession(loop=loop) as session:
        try:
            answer = await fetch(session, params)
        except Exception as msg:
            return (None,None,str(msg))
        return answer
