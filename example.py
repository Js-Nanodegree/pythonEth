import asyncio

from aiow3parity import ETH
from utils import send_request_aiohttp

wallet_eth = '0x7e07c035242eb6874460d8c033eee25a333988d1'
wallet_usdt = '0x3F9579D03d612E07dDc537feC32E8bb0Cc3cB58f'
url = "http://172.17.123.218:8545/"
smart_contract = '0xdAC17F958D2ee523a2206206994597C13D831ec7'


class Example:
    def __init__(self):
        self.loop = asyncio.get_event_loop()
        self.eth = ETH(
            send_request_aiohttp=send_request_aiohttp,
            log_function ="Log_Dir",
            smart_contract='0xdAC17F958D2ee523a2206206994597C13D831ec7',
            hw='0x2a1a93439242212f039Aa020f0e74169ec889e32',
            # host = "http://172.17.123.218:8545/",
            host='https://mainnet.infura.io/v3/698185618aa64a9f918c9bf9590520bd',
            key='0x00145ad01a3c93226fdf45d42221fe0f6810e610',
            currency_id=4,
            mnemonic='pager glorified chokehold slacking scenic abruptly synopses easter tackle pang nuttiness crummiest',
            passphrase='JOINMICROSTARK32131'
        )
        self.usdt = ETH(
            send_request_aiohttp=send_request_aiohttp,
            log_function="Log_Dir",
            smart_contract='0xdAC17F958D2ee523a2206206994597C13D831ec7',
            hw=[
                "0xe0f4Cd3dcC2DECA346bf4099E57f9771316E07C2",
                '0xe0f4Cd3dcC2DECA346bf4099E57f9771316E07C2',
                "0x2a1a93439242212f039Aa020f0e74169ec889e32",
                '0x2a1a93439242212f039Aa020f0e74169ec889e32'
            ],
            host="http://172.17.123.218:8545/",
            # host = 'https://mainnet.infura.io/v3/698185618aa64a9f918c9bf9590520bd',
            key='0x00145ad01a3c93226fdf45d42221fe0f6810e610',
            currency_id=7,
            mnemonic='pager glorified chokehold slacking scenic abruptly synopses easter tackle pang nuttiness crummiest',
            passphrase='JOINMICROSTARK321312'
        )
        self.address = [
            "0xe0f4Cd3dcC2DECA346bf4099E57f9771316E07C2",
            "0x2a1a93439242212f039Aa020f0e74169ec889e32",
        ]

    async def start(self):
        """
        ValueError: {'code': -32010, 'message': 'Transaction gas is too low.
        There is not enough gas to cover minimal cost of the transaction (minimal: 21584, got: 3).
        Try increasing supplied gas.'}
        :return:
        """

        # create Account
        data = await self.create_account()
        # print(data)

        # check_balance
        data = await self.check_ballance()
        # print(data)
        # check the syncked block
        data = await self.eth._get_block()
        data = await self.usdt._get_block()
        # check all account
        data = await self.all_account()
        # print(data)

        self.loop.call_later(
            3,
            self.loop.create_task,
            self.start()
        )

    async def all_account(self):
        body = ()
        # data = await self.eth.get_accounts(type='name')
        # data = await self.usdt.get_accounts(type='meta')
        data = await self.usdt.get_accounts(type='all')
        print(data)
        return 'All Accounts'

    async def create_account(self):
        remote_id = 'Trash'
        data = await self.eth.get_new_address(remote_id)
        print('eth',data)
        data = await self.eth._kill_address(address=data)
        return 'Create Account'

    async def check_ballance(self):
        for item in self.address:
            data = await self.usdt.get_balance(address = item)
            if data is not None:
                print('usdt',data)
            data = await self.eth.get_balance(address = item)
            if data is not None:
                print('eth',data)

        return 'CheckBallance'
    # async def send_transaction(self, body):
    #     (contract, address, value, gas) = body
    #     (address, value, smart) = await eth.check_ballance(address=self.address)
    #     if value == 0:
    #         # TODO Wait a transaction count
    #         return None
    #     else:
    #         body = (address, value, gas)
    #         data = await eth._create_transaction(body)
    #         try:
    #             send_transaction = await eth._send_raw_transaction(data)
    #         except Exception as msg:
    #             raise
    #     return send_transaction
