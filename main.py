import asyncio

from example import Example


async def main():
    print("server was started")
    loop = asyncio.get_running_loop()
    # unit = ETH()
    unit = Example()
    loop.create_task(unit.start())


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(main())
    print('aio-degree run forever')
    loop.run_forever()
