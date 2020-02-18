import asyncio
import json
from web3 import Web3
from utils import send_request_aiohttp
import abi
# url = "https://mainnet.infura.io/v3/698185618aa64a9f918c9bf9590520bd"

# abi = json.loads('[{"constant":true,"inputs":[],"name":"mintingFinished","outputs":[{"name":"","type":"bool"}],"payable":false,"type":"function"},{"constant":true,"inputs":[],"name":"name","outputs":[{"name":"","type":"string"}],"payable":false,"type":"function"},{"constant":false,"inputs":[{"name":"_spender","type":"address"},{"name":"_value","type":"uint256"}],"name":"approve","outputs":[],"payable":false,"type":"function"},{"constant":true,"inputs":[],"name":"totalSupply","outputs":[{"name":"","type":"uint256"}],"payable":false,"type":"function"},{"constant":false,"inputs":[{"name":"_from","type":"address"},{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"transferFrom","outputs":[],"payable":false,"type":"function"},{"constant":true,"inputs":[],"name":"decimals","outputs":[{"name":"","type":"uint256"}],"payable":false,"type":"function"},{"constant":false,"inputs":[],"name":"unpause","outputs":[{"name":"","type":"bool"}],"payable":false,"type":"function"},{"constant":false,"inputs":[{"name":"_to","type":"address"},{"name":"_amount","type":"uint256"}],"name":"mint","outputs":[{"name":"","type":"bool"}],"payable":false,"type":"function"},{"constant":true,"inputs":[],"name":"paused","outputs":[{"name":"","type":"bool"}],"payable":false,"type":"function"},{"constant":true,"inputs":[{"name":"_owner","type":"address"}],"name":"balanceOf","outputs":[{"name":"balance","type":"uint256"}],"payable":false,"type":"function"},{"constant":false,"inputs":[],"name":"finishMinting","outputs":[{"name":"","type":"bool"}],"payable":false,"type":"function"},{"constant":false,"inputs":[],"name":"pause","outputs":[{"name":"","type":"bool"}],"payable":false,"type":"function"},{"constant":true,"inputs":[],"name":"owner","outputs":[{"name":"","type":"address"}],"payable":false,"type":"function"},{"constant":true,"inputs":[],"name":"symbol","outputs":[{"name":"","type":"string"}],"payable":false,"type":"function"},{"constant":false,"inputs":[{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"transfer","outputs":[],"payable":false,"type":"function"},{"constant":false,"inputs":[{"name":"_to","type":"address"},{"name":"_amount","type":"uint256"},{"name":"_releaseTime","type":"uint256"}],"name":"mintTimelocked","outputs":[{"name":"","type":"address"}],"payable":false,"type":"function"},{"constant":true,"inputs":[{"name":"_owner","type":"address"},{"name":"_spender","type":"address"}],"name":"allowance","outputs":[{"name":"remaining","type":"uint256"}],"payable":false,"type":"function"},{"constant":false,"inputs":[{"name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"payable":false,"type":"function"},{"anonymous":false,"inputs":[{"indexed":true,"name":"to","type":"address"},{"indexed":false,"name":"value","type":"uint256"}],"name":"Mint","type":"event"},{"anonymous":false,"inputs":[],"name":"MintFinished","type":"event"},{"anonymous":false,"inputs":[],"name":"Pause","type":"event"},{"anonymous":false,"inputs":[],"name":"Unpause","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"owner","type":"address"},{"indexed":true,"name":"spender","type":"address"},{"indexed":false,"name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"from","type":"address"},{"indexed":true,"name":"to","type":"address"},{"indexed":false,"name":"value","type":"uint256"}],"name":"Transfer","type":"event"}]')
# user_address=['0x4E9dD5Eeda2Bee36a7c1FE6a90A349653D3EE19C','0x96E1c8eC4802F959A84a48f8b65A603f8Bd9A013','0x88b534121fa9D03CeA7a12d2F3CA8C8de8971697']
# address_smart_contract = '0xdAC17F958D2ee523a2206206994597C13D831ec7'
# contract = web3.eth.contract(address=address_smart_contract, abi=abi)
# data = web3.eth.accounts
# print(data)
#

wallet_eth='0x7e07c035242eb6874460d8c033eee25a333988d1'
wallet_usdt='0x3F9579D03d612E07dDc537feC32E8bb0Cc3cB58f'

class ETH:
    def __init__(self):
        self.loop = asyncio.get_event_loop()
        self.url = "http://172.17.123.218:8545/"
        self.web3 = Web3(Web3.HTTPProvider("http://172.17.123.218:8545/"))
        self.smart_contract = '0xdAC17F958D2ee523a2206206994597C13D831ec7'
        self.smart_contract = None

    # Start Entrypoint
    async def start(self):
        (mode,address,data) = await self.check_ballance(self.check_sum_address(address = wallet_eth))
        print(mode,address,data)
        (mode,address,data) = await self.check_ballance(self.check_sum_address(address = wallet_usdt))
        print(mode,address,data)
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

    async def check_ballance(self,address):
        '''
        Returns the balance of the given account at the block specified by block_identifier.
        account may be a checksum address or an ENS name
        :param address: Checksum Address
        :return:
        (address,ballance,smart_contract)
        '''
        connected = self.web3.isConnected()
        if connected == True:
            if self.smart_contract is None:
                ballance = self.web3.eth.getBalance(address)
                return (address,self.from_wei(ballance),None)
            else:
                contract = self.web3.eth.contract(address=self.smart_contract, abi=abi)
                ballance = contract.functions.balanceOf(address).call()
            return (address,self.from_wei(ballance),self.smart_contract)
        else:
            return (None,None,None)

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
        TODO NOT WORK WITH ADDRESS IN LOCAL BASE AND CREATE ADDRESS

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

    async def send_signed_transaction(self,address):
        # Special Note: The nonce=self.eth.getTransactionCount(self.eth.coinbase) here is to get the number of transactions sent from this address!
        # nonce is unique, if it is not unique, it will fail!
        nonce = self.eth.getTransactionCount(self.eth.coinbase)
        gasPrice = self.eth.gasPrice

        signed_txn = self.eth.account.signTransaction(dict(
            nonce=nonce,
            gasPrice=gasPrice,
            gas=100000,
            to=address,
            value=11,
            data=b'',
            chainId=3
        ), "0xee9eb15a7f063b484355e7372bcbcff186bc6a9aa9575cd5b26fda323fc72f45")

        signed = self.eth.sendRawTransaction(signed_txn.rawTransaction);
        print(signed);
        return signed

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

    async def parity_localTransactions(self):
        '''
        parity_localTransactionsОн возвращает объект, хэш-ключ для сделки, стоимость сделки объекта
        :return:
        (200,{
              "id": 1,
              "jsonrpc": "2.0",
              "result": {
                "0x09e64eb1ae32bb9ac415ce4ddb3dbad860af72d9377bb5f073c9628ab413c532": {
                  "status": "mined",
                  "transaction": {
                    "from": "0x00a329c0648769a73afac7f9381e08fb43dbea72",
                    "to": "0x00a289b43e1e4825dbedf2a78ba60a640634dc40",
                    "value": "0xfffff",
                    "blockHash": null,
                    "blockNumber": null,
                    "creates": null,
                    "gas": "0xe57e0",
                    "gasPrice": "0x2d20cff33",
                    "hash": "0x09e64eb1ae32bb9ac415ce4ddb3dbad860af72d9377bb5f073c9628ab413c532",
                    "input": "0x",
                    "condition": {
                      "block": 1
                    },
                    "chainId": null,
                    "nonce": "0x0",
                    "publicKey": "0x3fa8c08c65a83f6b4ea3e04e1cc70cbe3cd391499e3e05ab7dedf28aff9afc538200ff93e3f2b2cb5029f03c7ebee820d63a4c5a9541c83acebe293f54cacf0e",
                    "raw": "0xf868808502d20cff33830e57e09400a289b43e1e4825dbedf2a78ba60a640634dc40830fffff801ca034c333b0b91cd832a3414d628e3fea29a00055cebf5ba59f7038c188404c0cf3a0524fd9b35be170439b5ffe89694ae0cfc553cb49d1d8b643239e353351531532",
                    "standardV": "0x1",
                    "v": "0x1c",
                    "r": "0x34c333b0b91cd832a3414d628e3fea29a00055cebf5ba59f7038c188404c0cf3",
                    "s": "0x524fd9b35be170439b5ffe89694ae0cfc553cb49d1d8b643239e353351531532",
                    "transactionIndex": null
                  }
                },
                "0x...": { ... }
              }
            })
        '''
        data = (1, 'parity_localTransactions', [])
        params = self.create_params(data)
        try:
            answer = await self.request_node(params)
        except Exception as msg:
            #   TODO CHECK THIS LOG FILE
            # raise
            return (500, str(msg))
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
        correct_address = self.web3.isAddress(address)
        if correct_address == True:
            address = self.web3.toChecksumAddress(address)
            return address
        else:
            return None

    def from_wei(self,ballance):
        if self.smart_contract is None:
            return self.web3.fromWei(ballance,'ether')
        else:
            return self.web3.fromWei(ballance,'mwei')

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
