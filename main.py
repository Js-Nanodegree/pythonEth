import asyncio
import json

from web3 import Web3

import abi
from utils import send_request_aiohttp

url = "https://mainnet.infura.io/v3/698185618aa64a9f918c9bf9590520bd"

# abi = json.loads('[{"constant":true,"inputs":[],"name":"mintingFinished","outputs":[{"name":"","type":"bool"}],"payable":false,"type":"function"},{"constant":true,"inputs":[],"name":"name","outputs":[{"name":"","type":"string"}],"payable":false,"type":"function"},{"constant":false,"inputs":[{"name":"_spender","type":"address"},{"name":"_value","type":"uint256"}],"name":"approve","outputs":[],"payable":false,"type":"function"},{"constant":true,"inputs":[],"name":"totalSupply","outputs":[{"name":"","type":"uint256"}],"payable":false,"type":"function"},{"constant":false,"inputs":[{"name":"_from","type":"address"},{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"transferFrom","outputs":[],"payable":false,"type":"function"},{"constant":true,"inputs":[],"name":"decimals","outputs":[{"name":"","type":"uint256"}],"payable":false,"type":"function"},{"constant":false,"inputs":[],"name":"unpause","outputs":[{"name":"","type":"bool"}],"payable":false,"type":"function"},{"constant":false,"inputs":[{"name":"_to","type":"address"},{"name":"_amount","type":"uint256"}],"name":"mint","outputs":[{"name":"","type":"bool"}],"payable":false,"type":"function"},{"constant":true,"inputs":[],"name":"paused","outputs":[{"name":"","type":"bool"}],"payable":false,"type":"function"},{"constant":true,"inputs":[{"name":"_owner","type":"address"}],"name":"balanceOf","outputs":[{"name":"balance","type":"uint256"}],"payable":false,"type":"function"},{"constant":false,"inputs":[],"name":"finishMinting","outputs":[{"name":"","type":"bool"}],"payable":false,"type":"function"},{"constant":false,"inputs":[],"name":"pause","outputs":[{"name":"","type":"bool"}],"payable":false,"type":"function"},{"constant":true,"inputs":[],"name":"owner","outputs":[{"name":"","type":"address"}],"payable":false,"type":"function"},{"constant":true,"inputs":[],"name":"symbol","outputs":[{"name":"","type":"string"}],"payable":false,"type":"function"},{"constant":false,"inputs":[{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"transfer","outputs":[],"payable":false,"type":"function"},{"constant":false,"inputs":[{"name":"_to","type":"address"},{"name":"_amount","type":"uint256"},{"name":"_releaseTime","type":"uint256"}],"name":"mintTimelocked","outputs":[{"name":"","type":"address"}],"payable":false,"type":"function"},{"constant":true,"inputs":[{"name":"_owner","type":"address"},{"name":"_spender","type":"address"}],"name":"allowance","outputs":[{"name":"remaining","type":"uint256"}],"payable":false,"type":"function"},{"constant":false,"inputs":[{"name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"payable":false,"type":"function"},{"anonymous":false,"inputs":[{"indexed":true,"name":"to","type":"address"},{"indexed":false,"name":"value","type":"uint256"}],"name":"Mint","type":"event"},{"anonymous":false,"inputs":[],"name":"MintFinished","type":"event"},{"anonymous":false,"inputs":[],"name":"Pause","type":"event"},{"anonymous":false,"inputs":[],"name":"Unpause","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"owner","type":"address"},{"indexed":true,"name":"spender","type":"address"},{"indexed":false,"name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"from","type":"address"},{"indexed":true,"name":"to","type":"address"},{"indexed":false,"name":"value","type":"uint256"}],"name":"Transfer","type":"event"}]')
# user_address=['0x4E9dD5Eeda2Bee36a7c1FE6a90A349653D3EE19C','0x96E1c8eC4802F959A84a48f8b65A603f8Bd9A013','0x88b534121fa9D03CeA7a12d2F3CA8C8de8971697']
# address_smart_contract = '0xdAC17F958D2ee523a2206206994597C13D831ec7'
# contract = web3.eth.contract(address=address_smart_contract, abi=abi)
# data = web3.eth.accounts
# print(data)
#
class ETH:
    def __init__(self):
        self.loop = asyncio.get_event_loop()
        self.url = "http://172.17.221.163:8545/"
        self.web3 = Web3(Web3.HTTPProvider("http://172.17.221.163:8545/"))
        self.smart_contract = '0xdAC17F958D2ee523a2206206994597C13D831ec7'
        self.smart_contract = None

    # Start Entrypoint
    async def start(self):
        # (mode,address,label) = await self.create_address('Slava','Slava')
        # print(address)
        print('start')
        return True

    # Curremt Library Method For NODE  ETHERIUM
    async def create_address(self,phrase,label):
        '''
        this method create Eth Address and set Label for address
        :param phrase:  Take in Config password phase
        :param label: Remote ID
        :return:
        (current_contract ,address_wallet, label_wallet)
        '''
        # create address
        if self.smart_contract is None:
            print('create account Eth')
            address = self.web3.parity.personal.newAccount(phrase)
        else:
            print('create account Tether')
            address = 'Tether'
        # set label for address
        body = [address, label]
        label_account = await self.parity_setAccountName(body)
        # create task for check_ballance()
        (code,data) = label_account
        if code == 200:
            if data['result'] == True:
                return (self.smart_contract,address,label)
            else:
                return (self.smart_contract,address,None)
        elif code == 500:
           return (self.smart_contract,address, data)

    async def take_list_address(self):
        '''
        if using web3.py we take all address work in currnet node
        if using RPC.API parity_allAccountsInfo we take all address with detail info
            {name:'Example',meta:'Something',UUID:'Some Number Hex'}

        :return:
        [address_eth_isUpperCase, ..., ...]
        '''
        # return all address in current wallet
        list = self.web3.parity.personal.listAccounts()
        # list = await self.parity_allAccountsInfo()
        return list

    async def find_address_name(self,address):
        '''
        find name label in address when user are send

        :param address: '0xF4D34Bb387a65B459d065238A3f093A89cB54e30'
        :return:
        (address,name_address)
        (500,Error message)
        '''
        data = (1, 'parity_accountsInfo', [])
        params = self.create_params(data)
        try:
            answer = await self.request_node(params)
        except Exception as msg:
            #   TODO CHECK THIS LOG FILE
            # raise
            return (500, str(msg))
        (code,data) = answer
        name = data['result']
        return (address,name[address])

    async def send_transaqtion(self):
        # if this transaqtion is not blocked
        # return hash transaqtion
        return 'dfkjhgnkjdsfnksdjfkjsd%^SA&5d'

    # RPC API REQUEST FOR NODE ETHERIUM
    async def parity_setAccountName(self,body):
        data = (1, 'parity_setAccountName', body)
        params = self.create_params(data)
        try:
            answer = await self.request_node(params)
        except Exception as msg:
            #   TODO CHECK THIS LOG FILE
            # raise
            return (500,str(msg))
        return answer

    async def gas_transaqtion(self):
        # return how much eth need to transaqtion
        return 2.15

    async def notify_other(self):
        # send to matchenger and other resources
        return 'Ok'

    # Helper for Request for crypto Nodes Etherium
    def create_params(self, body):
        '''
        Create Params for aiohttp request
        :param body: (key_request,method_callable,args_request)
        :return:

        '''
        (key, method, args) = body
        params = {
            'method': 'POST',
            'headers': {'content-type': 'application/json'},
            'data': json.dumps({"jsonrpc": "2.0", "id": key, "method": method, "params": args})
        }
        params['url'] = self.url
        return params

    async def request_node(self, params):
        '''
        send request for aiohttp and fetch answer data in CryptoNodes ETH
        :param params: create with method create_params
        :return:
        (code,data['result'])
        (200,'Ok')
        '''
        answer = await send_request_aiohttp(params)
        (mode, code, data) = answer
        if code is None:
            return (None, data)
        elif code == 200:
            return (code, data)
        else:
            return (code, mode)

    # Helper Utils for request Eth Node
    def check_sum_address(self,address):
        '''
        Will convert an upper or lowercase Ethereum address to a checksum address.

        :param address:
        :return:
        '''
        correct_address = web3.isAddress(address)
        if correct_address == True:
            address = self.web3.toChecksumAddress(address)
            return address
        else:
            return None

    def hex_to_string(self,hex):
        '''
        Returns the number representation of a given HEX value as a string.
        :param hex: 0xea
        :return:
        "234"
        '''
        answer = self.web3.hexToNumberString(hex)
        return answer

    def number_to_hex(self,number):
        '''
        Returns the HEX representation of a given number value.
        :param number: "234"
        :return:
        0xea
        '''
        answer = self.web3.numberToHex(number)
        return answer



async def main():
    print('server was started')
    loop = asyncio.get_running_loop()
    unit = ETH()
    loop.create_task(unit.start())


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(main())
    print('aio-degree run forever')
    loop.run_forever()
