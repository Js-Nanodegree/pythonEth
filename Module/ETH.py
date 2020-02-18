import asyncio
import json

from web3 import Web3

import abi
from utils import send_request_aiohttp

wallet_eth='0x7e07c035242eb6874460d8c033eee25a333988d1'
wallet_usdt='0x3F9579D03d612E07dDc537feC32E8bb0Cc3cB58f'
url = "http://172.17.123.218:8545/"
smart_contract = '0xdAC17F958D2ee523a2206206994597C13D831ec7'

class ETH:
    def __init__(self):
        self.loop = asyncio.get_event_loop()
        self.url = url
        self.web3 = Web3(Web3.HTTPProvider(url))
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

    async def create_transaction(self,body):
        '''
        If the transaction specifies a data value but does not specify gas
        then the gas value will be populated using the estimateGas()
        function with an additional buffer of 100000 gas up to the gasLimit of the latest block.
        In the event that the value returned by estimateGas()
        method is greater than the gasLimit a ValueError will be raised.
        :param body: (address,value,gas)
        :return:
        Returns a transaction that’s been signed by the node’s private key, but not yet submitted.
        The signed tx can be submitted with Eth.sendRawTransaction`
        '''
        (address,value,gas) = body
        transaction = {
            'to': address,
            'value': value,
            'gas': gas,
            'gasPrice': self.web3.eth.gasPrice,
            'nonce': self.web3.eth.getTransactionCount(self.web3.eth.coinbase),
            'chainId': 1
        }
        print(transaction)
        return transaction

    async def send_raw_transaction(self,transaction):
        '''
        Returns a transaction that’s been signed by the node’s private key, but not yet submitted. The signed tx can be submitted with Eth.sendRawTransaction`
        Sends a signed and serialized transaction. Returns the transaction hash as a HexBytes object.
        :param transaction: form create raw transaction
        :return:
        HexBytes('0xe670ec64341771606e55d6b4ca35a1a6b75ee3d5145a99d05921026d1527331')
        '''
        create_raw_transaction = self.web3.eth.account.sign_transaction(transaction, self.key)
        try:
            send_raw_transaction = self.web3.eth.sendRawTransaction(create_raw_transaction.rawTransaction)
        except Exception as msg:
           raise

        return (200, send_raw_transaction)

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
