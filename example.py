import asyncio
import json

from web3 import Web3

from Module.ETH import ETH

wallet_eth = '0x7e07c035242eb6874460d8c033eee25a333988d1'
wallet_usdt = '0x3F9579D03d612E07dDc537feC32E8bb0Cc3cB58f'
url = "http://172.17.123.218:8545/"
smart_contract = '0xdAC17F958D2ee523a2206206994597C13D831ec7'

abi = json.loads(
    '[{"constant":true,"inputs":[],"name":"mintingFinished","outputs":[{"name":"","type":"bool"}],"payable":false,"type":"function"},{"constant":true,"inputs":[],"name":"name","outputs":[{"name":"","type":"string"}],"payable":false,"type":"function"},{"constant":false,"inputs":[{"name":"_spender","type":"address"},{"name":"_value","type":"uint256"}],"name":"approve","outputs":[],"payable":false,"type":"function"},{"constant":true,"inputs":[],"name":"totalSupply","outputs":[{"name":"","type":"uint256"}],"payable":false,"type":"function"},{"constant":false,"inputs":[{"name":"_from","type":"address"},{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"transferFrom","outputs":[],"payable":false,"type":"function"},{"constant":true,"inputs":[],"name":"decimals","outputs":[{"name":"","type":"uint256"}],"payable":false,"type":"function"},{"constant":false,"inputs":[],"name":"unpause","outputs":[{"name":"","type":"bool"}],"payable":false,"type":"function"},{"constant":false,"inputs":[{"name":"_to","type":"address"},{"name":"_amount","type":"uint256"}],"name":"mint","outputs":[{"name":"","type":"bool"}],"payable":false,"type":"function"},{"constant":true,"inputs":[],"name":"paused","outputs":[{"name":"","type":"bool"}],"payable":false,"type":"function"},{"constant":true,"inputs":[{"name":"_owner","type":"address"}],"name":"balanceOf","outputs":[{"name":"balance","type":"uint256"}],"payable":false,"type":"function"},{"constant":false,"inputs":[],"name":"finishMinting","outputs":[{"name":"","type":"bool"}],"payable":false,"type":"function"},{"constant":false,"inputs":[],"name":"pause","outputs":[{"name":"","type":"bool"}],"payable":false,"type":"function"},{"constant":true,"inputs":[],"name":"owner","outputs":[{"name":"","type":"address"}],"payable":false,"type":"function"},{"constant":true,"inputs":[],"name":"symbol","outputs":[{"name":"","type":"string"}],"payable":false,"type":"function"},{"constant":false,"inputs":[{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"transfer","outputs":[],"payable":false,"type":"function"},{"constant":false,"inputs":[{"name":"_to","type":"address"},{"name":"_amount","type":"uint256"},{"name":"_releaseTime","type":"uint256"}],"name":"mintTimelocked","outputs":[{"name":"","type":"address"}],"payable":false,"type":"function"},{"constant":true,"inputs":[{"name":"_owner","type":"address"},{"name":"_spender","type":"address"}],"name":"allowance","outputs":[{"name":"remaining","type":"uint256"}],"payable":false,"type":"function"},{"constant":false,"inputs":[{"name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"payable":false,"type":"function"},{"anonymous":false,"inputs":[{"indexed":true,"name":"to","type":"address"},{"indexed":false,"name":"value","type":"uint256"}],"name":"Mint","type":"event"},{"anonymous":false,"inputs":[],"name":"MintFinished","type":"event"},{"anonymous":false,"inputs":[],"name":"Pause","type":"event"},{"anonymous":false,"inputs":[],"name":"Unpause","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"owner","type":"address"},{"indexed":true,"name":"spender","type":"address"},{"indexed":false,"name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"from","type":"address"},{"indexed":true,"name":"to","type":"address"},{"indexed":false,"name":"value","type":"uint256"}],"name":"Transfer","type":"event"}]'
)


class Example:
    def __init__(self):
        self.loop = asyncio.get_event_loop()
        self.url = url
        self.web3 = Web3(Web3.HTTPProvider(url))
        self.key = '0x4c0883a69102937d6231471b5dbb6204fe5129617082792ae468d01a3f362318'
        self.address = '0x91a300C11833d906aC811B4a0C3B93D9f0A83E24',
        self.passphrase = 'JOINMICROSTARK'

    async def start(self):
        '''
        ValueError: {'code': -32010, 'message': 'Transaction gas is too low.
        There is not enough gas to cover minimal cost of the transaction (minimal: 21584, got: 3).
        Try increasing supplied gas.'}
        :return:
        '''
        # eth = ETH(None)

        eth = ETH(
            loop = asyncio.get_event_loop(),
            smart_contract = '0xdAC17F958D2ee523a2206206994597C13D831ec7',
            HW = '',
            url = "http://172.17.123.218:8545/",
            key = '0x00145ad01a3c93226fdf45d42221fe0f6810e610',
            mnemonc = 'pager glorified chokehold slacking scenic abruptly synopses easter tackle pang nuttiness crummiest',
            passphrase = 'JOINMICROSTARK'
        )
        # body = ('0x91a300C11833d906aC811B4a0C3B93D9f0A83E24',
        #         '0x91a300C11833d906aC811B4a0C3B93D9f0A83E24', 123, 12)
        # body = ('0x91a300C11833d906aC811B4a0C3B93D9f0A83E24')
        # data = await eth.take_list_address(body)
        body=(self.passphrase,'UW')
        data = await eth.create_address(body)
        print(data)
        # (contract, address, label) = await eth.create_address('Kirkoroff', 'VIRTEKPAYTEST')
        # print(contract, address, label)
        # if address is None:
        #     return 'Error in create Account try again'
        # address = ['0x91a300C11833d906aC811B4a0C3B93D9f0A83E24',
        #            '0x888a006d2794320c780eCdbE359f9C16982A86e8']

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

# поддержка 2 уровня поддержки jivosite вебвизор мессанджеры аналитика
# yandex metrica yandex webvisor google tag manager
