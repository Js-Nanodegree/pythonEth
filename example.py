# >>> transaction = {
# ...     'to': '0xF0109fC8DF283027b6285cc889F5aA624EaC1F55',
# ...     'value': 1000000000,
# ...     'gas': 2000000,
# ...     'gasPrice': 234567897654321,
# ...     'nonce': 0,
# ...     'chainId': 1
# ... }
# >>> key = '0x4c0883a69102937d6231471b5dbb6204fe5129617082792ae468d01a3f362318'
# >>> signed = w3.eth.account.sign_transaction(transaction, key)
# >>> signed.rawTransaction
# HexBytes('0xf86a8086d55698372431831e848094f0109fc8df283027b6285cc889f5aa624eac1f55843b9aca008025a009ebb6ca057a0535d6186462bc0b465b561c94a295bdb0621fc19208ab149a9ca0440ffd775ce91a833ab410777204d5341a6f9fa91216a6f3ee2c051fea6a0428')
# >>> signed.hash
# HexBytes('0xd8f64a42b57be0d565f385378db2f6bf324ce14a594afc05de90436e9ce01f60')
# >>> signed.r
# 4487286261793418179817841024889747115779324305375823110249149479905075174044
# >>> signed.s
# 30785525769477805655994251009256770582792548537338581640010273753578382951464
# >>> signed.v
# 37

# # When you run sendRawTransaction, you get back the hash of the transaction:
# >>> w3.eth.sendRawTransaction(signed.rawTransaction)
# # '0xd8f64a42b57be0d565f385378db2f6bf324ce14a594afc05de90436e9ce01f60'

import asyncio
import json

from web3 import Web3

import abi
from utils import send_request_aiohttp


wallet_eth='0x7e07c035242eb6874460d8c033eee25a333988d1'
wallet_usdt='0x3F9579D03d612E07dDc537feC32E8bb0Cc3cB58f'
url = "http://172.17.123.218:8545/"
smart_contract = '0xdAC17F958D2ee523a2206206994597C13D831ec7'

class Example:
    def __init__(self):
        self.loop = asyncio.get_event_loop()
        self.url = url
        self.web3 = Web3(Web3.HTTPProvider(url))
        self.smart_contract = '0xdAC17F958D2ee523a2206206994597C13D831ec7'
        self.smart_contract = None
        self.key = '0x4c0883a69102937d6231471b5dbb6204fe5129617082792ae468d01a3f362318'

    async def start(self):
        body = ('0xd3CdA913deB6f67967B99D67aCDFa1712C293601', 500, 3)
        transaction = await self.create_transaction(body)
        data = await self.send_raw_transaction(transaction)
        print(data)
        return True

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
