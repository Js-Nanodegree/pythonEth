import asyncio
import json

from web3 import Web3

import abi
from utils import send_request_aiohttp

wallet_eth = '0x7e07c035242eb6874460d8c033eee25a333988d1'
wallet_usdt = '0x3F9579D03d612E07dDc537feC32E8bb0Cc3cB58f'
url = "http://172.17.123.218:8545/"
smart_contract = '0xdAC17F958D2ee523a2206206994597C13D831ec7'

error = {
    'Web3_Not_Work': {'code': '-200', 'mode': 'Connct to reserved address'},

}

class ETH:
    def __init__(self):
        self.loop = asyncio.get_event_loop()
        self.url = url
        self.web3 = Web3(Web3.HTTPProvider(url))
        self.smart_contract = '0xdAC17F958D2ee523a2206206994597C13D831ec7'
        self.smart_contract = None
        self.key = '0x4c0883a69102937d6231471b5dbb6204fe5129617082792ae468d01a3f362318'
        self.passphrase = 'JOINMICROSTARK'

    # Start Entrypoint
    async def start(self):
        (mode,address,data) = await self.check_ballance(self._check_sum_address(address = wallet_eth))
        print(mode,address,data)
        (mode,address,data) = await self.check_ballance(self._check_sum_address(address = wallet_usdt))
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
        address = self.web3.parity.personal.newAccount(phrase)
        # set label for address
        body = [address, label]
        label_account = await self._parity_setAccountName(body)
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
        if self._check_web3_connected() == True:
            '''
            connect with Web3 for main Node
            '''
            if self.smart_contract is None:
                ballance = self.web3.eth.getBalance(address)
                return (address, self._from_wei(ballance), None)
            else:
                contract = self._build_contract_usdt()
                ballance = contract.functions.balanceOf(address).call()
                return (address, self._from_wei(ballance), self.smart_contract)
        else:
            '''
            Need Connect to Reserved Node
            '''
            return (None, None, None)

    async def take_list_address(self):
        '''
        if using web3.py we take all address work in currnet node
        if using RPC.API parity_allAccountsInfo we take all address with detail info
            {name:'Example',meta:'Something',UUID:'Some Number Hex'}

        :return:
        [address_eth_isUpperCase, ..., ...]
        '''
        # return all address in current wallet
        # list = self.web3.parity.personal.listAccounts()
        all_list = await self.parity_allAccountsInfo()
        
        return all_list

    async def send_transaction(self, body):
        '''
        WARN rpc  eth_sendTransaction is deprecated and will be removed in future versions:
        Account management is being phased out see #9997 for alternatives.
        :param body:(send_to_wallet,send_from_wallet,value_send)
        :return:
        (code, hash_trx)
        '''
        (send_to_wallet, send_from_wallet, value_send) = body
        try:
            if self.smart_contract is None:
                hash = self.web3.eth.sendTransaction(
                    {'to': send_to_wallet, 'from': send_from_wallet, 'value': value_send})
            else:
                # TODO SEARCH METHOD SEND TRANSACTION FOR ERC20
                hash = None
        except Exception as msg:
            return (None,str(msg))

        return (200,hash)

    async def _send_raw_transaction(self, transaction):
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
    async def _parity_setAccountName(self, body):
        data = (1, 'parity_setAccountName', body)
        params = self._create_params(data)
        try:
            answer = await self._request_node(params)
        except Exception as msg:
            #   TODO CHECK THIS LOG FILE
            # raise
            return (500, str(msg))
        return answer

    async def _unlock_account(self, body):
        '''
        Unlocks the given account for duration seconds.
        If duration is None then the account will remain unlocked indefinitely.
        Returns boolean as to whether the account was successfully unlocked.
        :param body: (address,passphrase)
        :return:
        (code,Boolean)
        '''
        (address, passphrase) = body
        try:
            logic = self.web3.parity.personal.unlockAccount(address,passphrase)
        except Exception as msg:
            print(str(msg))
            return (msg['code'],msg['message'],msg['message'])
        return (200,logic)

    # Helper for Request for crypto Nodes Etherium
    def _create_params(self, body):
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

    def _create_gas_params(self):
        '''
        Create Params for aiohttp request
        :return
        [
            {
                gasprice: 40,
                hashpower_accepting: 100,
                hashpower_accepting2: 97.6744186047,
                tx_atabove: 3,
                age: 0,
                pct_remaining5m: 0,
                pct_mined_5m: 100,
                total_seen_5m: 1,
                average: 400,
                safelow: 100,
                nomine: null,
                avgdiff: 1,
                intercept: 4.8015,
                hpa_coef: -0.0243,
                avgdiff_coef: -1.6459,
                tx_atabove_coef: 0.0006,
                int2: 6.9238,
                hpa_coef2: -0.067,
                sum: 0.2238,
                expectedWait: 2,
                unsafe: 0,
                expectedTime: 0.52
            }
        ]
        '''
        (key, method, args) = body
        params = {
            'method': 'GET',
        }
        params['url'] = 'https://ethgasstation.info/json/ethgasAPI.json'
        return params

    async def _create_transaction(self, body):
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
        nonce = _take_nonce(address)
        gasPrice = self.web3.eth.gasPrice

        if self.smart_contract is None:
            transaction = {
                'chainId': 1,
                'to': address,
                'value': value,
                'gas': gas,
                'gasPrice': gasPrice,
                'nonce': nonce,
            }
        else:
            contract = self._build_contract_usdt()
            transaction = contract.functions.transfer(address, value).buildTransaction({
                    'chainId': 1,
                    'gas': gas,
                    'gasPrice': gasPrice,
                    'nonce': nonce,
            })

        return transaction

    async def _request_node(self, params):
        '''
        send request for aiohttp and fetch answer data in CryptoNodes ETH
        :param params: create with method _create_params
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
    def _check_web3_connected(self):
        return self.web3.isConnected()

    def _check_sum_address(self, address):
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

    def _take_nonce(self, address):
        '''
        Last famous transaction id block for create transaction Id
        :return:
        number
        '''
        if address is None:
            address = self.web3.eth.coinbase
        nonce = self.web3.eth.getTransactionCount(address)
        return nonce

    def _build_contract_usdt(self):
        return self.web3.eth.contract(address=self.smart_contract, abi=abi)

    def _from_wei(self, ballance):
        if self.smart_contract is None:
            return self.web3.fromWei(ballance, 'ether')
        else:
            return self.web3.fromWei(ballance, 'mwei')

    def _hex_to_string(self, hex):
        '''
        Returns the number representation of a given HEX value as a string.
        :param hex: 0xea
        :return:
        "234"
        '''
        return self.web3.hexToNumberString(hex)

    def _number_to_hex(self, number):
        '''
        Returns the HEX representation of a given number value.
        :param number: "234"
        :return:
        0xea
        '''
        return self.web3.numberToHex(number)