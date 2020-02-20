import asyncio
import json

from web3 import Web3

from utils import send_request_aiohttp

abi = json.loads(
    '[{"constant":true,"inputs":[],"name":"mintingFinished","outputs":[{"name":"","type":"bool"}],"payable":false,"type":"function"},{"constant":true,"inputs":[],"name":"name","outputs":[{"name":"","type":"string"}],"payable":false,"type":"function"},{"constant":false,"inputs":[{"name":"_spender","type":"address"},{"name":"_value","type":"uint256"}],"name":"approve","outputs":[],"payable":false,"type":"function"},{"constant":true,"inputs":[],"name":"totalSupply","outputs":[{"name":"","type":"uint256"}],"payable":false,"type":"function"},{"constant":false,"inputs":[{"name":"_from","type":"address"},{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"transferFrom","outputs":[],"payable":false,"type":"function"},{"constant":true,"inputs":[],"name":"decimals","outputs":[{"name":"","type":"uint256"}],"payable":false,"type":"function"},{"constant":false,"inputs":[],"name":"unpause","outputs":[{"name":"","type":"bool"}],"payable":false,"type":"function"},{"constant":false,"inputs":[{"name":"_to","type":"address"},{"name":"_amount","type":"uint256"}],"name":"mint","outputs":[{"name":"","type":"bool"}],"payable":false,"type":"function"},{"constant":true,"inputs":[],"name":"paused","outputs":[{"name":"","type":"bool"}],"payable":false,"type":"function"},{"constant":true,"inputs":[{"name":"_owner","type":"address"}],"name":"balanceOf","outputs":[{"name":"balance","type":"uint256"}],"payable":false,"type":"function"},{"constant":false,"inputs":[],"name":"finishMinting","outputs":[{"name":"","type":"bool"}],"payable":false,"type":"function"},{"constant":false,"inputs":[],"name":"pause","outputs":[{"name":"","type":"bool"}],"payable":false,"type":"function"},{"constant":true,"inputs":[],"name":"owner","outputs":[{"name":"","type":"address"}],"payable":false,"type":"function"},{"constant":true,"inputs":[],"name":"symbol","outputs":[{"name":"","type":"string"}],"payable":false,"type":"function"},{"constant":false,"inputs":[{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"transfer","outputs":[],"payable":false,"type":"function"},{"constant":false,"inputs":[{"name":"_to","type":"address"},{"name":"_amount","type":"uint256"},{"name":"_releaseTime","type":"uint256"}],"name":"mintTimelocked","outputs":[{"name":"","type":"address"}],"payable":false,"type":"function"},{"constant":true,"inputs":[{"name":"_owner","type":"address"},{"name":"_spender","type":"address"}],"name":"allowance","outputs":[{"name":"remaining","type":"uint256"}],"payable":false,"type":"function"},{"constant":false,"inputs":[{"name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"payable":false,"type":"function"},{"anonymous":false,"inputs":[{"indexed":true,"name":"to","type":"address"},{"indexed":false,"name":"value","type":"uint256"}],"name":"Mint","type":"event"},{"anonymous":false,"inputs":[],"name":"MintFinished","type":"event"},{"anonymous":false,"inputs":[],"name":"Pause","type":"event"},{"anonymous":false,"inputs":[],"name":"Unpause","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"owner","type":"address"},{"indexed":true,"name":"spender","type":"address"},{"indexed":false,"name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"from","type":"address"},{"indexed":true,"name":"to","type":"address"},{"indexed":false,"name":"value","type":"uint256"}],"name":"Transfer","type":"event"}]')

# wallet_eth = '0x7e07c035242eb6874460d8c033eee25a333988d1'
# wallet_usdt = '0x3F9579D03d612E07dDc537feC32E8bb0Cc3cB58f'
# url = "http://172.17.123.218:8545/"
# smart_contract = '0xdAC17F958D2ee523a2206206994597C13D831ec7'
#
# error = {
#     'Web3_Not_Work': {'code': '-200', 'mode': 'Connct to reserved address'},
# }


class ETH:
    def __init__(self, loop, smart_contract, HW, url, key, mnemonc, passphrase):
        self.loop = asyncio.get_event_loop()
        self.smart_contract = smart_contract
        self.HW = HW
        self.url = url
        self.key = key
        self.mnemonc = mnemonc
        self.passphrase = passphrase
        self.web3 = Web3(Web3.HTTPProvider(url))

    # Curremt Library Method For NODE  ETHERIUM
    async def create_address(self, body):
        '''
        this method create Eth Address and set Label for address
        :param body: (phrase, label) => (Take in Config password phase, Remote ID)
        :return:
        (current_contract ,address_wallet, label_wallet)
        (200, '0x967a9C9f42ccC2891Cf89731E6D4F1279C0dB9d7', 'HW')
        '''
        # create address
        (phrase, label) = body
        address = self.web3.parity.personal.newAccount(self.passphrase)

        # set label for address
        body = (address, self.passphrase)

        (code, mode, data) = await self._unlock_account(body)
        if code is None:
            data = await self._kill_account(address, phrase)
            return (data, 'Unlock Account', 'Account is Lock')

        elif code == 200:
            body = [self._check_sum_address(address), label]
            (code, mode, data) = await self._parity_setAccountName(body)

            if code == 200:
                if data['result'] == True:
                    return (code, address, label)
                else:
                    return (code, address, None)
        else:
            data = await self._kill_account(address, phrase)
            return (data, mode, data)

    async def check_ballance(self, address):
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
                ballance = self.web3.eth.getBalance(
                    self._check_sum_address(address))
                return (address, self._from_wei(ballance), None)
            else:
                contract = self._build_contract_usdt()
                ballance = contract.functions.balanceOf(
                    self._check_sum_address(address)).call()
                return (address, self._from_wei(ballance), self.smart_contract)
        else:
            '''
            Need Connect to Reserved Node
            '''
            return (None, 'WEB3 IS NOT WORKING', None)

    async def take_list_address(self, body):
        '''
        if using web3.py we take all address work in currnet node
        if using RPC.API parity_allAccountsInfo we take all address with detail info
            {name:'Example',meta:'Something',UUID:'Some Number Hex'}

        :return:
        [address_eth_isUpperCase, ..., ...]
        '''
        responce = {}
        (hw) = body
        (code, mode, data) = await self._parity_allAccountsInfo()
        for (x, i) in data['result'].items():
            responce[x] = i['name']
        # responce.remove(hw)

        return (code, mode, responce)

    async def send_transaction(self, body):
        """
        Method Create Send Transaction with RawTransaction
        :param body:
        contract = None || smart-contract
        to_address = send to wallet
        from_address = who send to wallet
        value = ballance userwallet
        gas = value gas
        :return:
        200 = code status
        trx_hash = trx_hash
        value = ballance-sender
        """
        (to_address, from_address, value, gas) = body
        (_, value, _) = await self.check_ballance(address=from_address)
        if value == 0:
            # TODO Wait a transaction count
            return (200, None, value)
        else:
            body = (to_address, value, gas)
            trx = await self._create_transaction(body)
            try:
                trx_hash = await self._send_raw_transaction(trx)
            except Exception as msg:
                return (500, str(msg), value)
        return (200, trx_hash, value)

    async def _send_raw_transaction(self, transaction):
        '''
        Returns a transaction that’s been signed by the node’s private key, but not yet submitted. The signed tx can be submitted with Eth.sendRawTransaction`
        Sends a signed and serialized transaction. Returns the transaction hash as a HexBytes object.
        :param transaction: form create raw transaction
        :return:
        HexBytes('0xe670ec64341771606e55d6b4ca35a1a6b75ee3d5145a99d05921026d1527331')
        '''
        create_raw_transaction = self.web3.eth.account.sign_transaction(
            transaction, self.key)
        try:
            send_raw_transaction = self.web3.eth.sendRawTransaction(
                create_raw_transaction.rawTransaction)
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
            return (None, 'Label Not Set', str(msg))
        return answer

    async def _parity_allAccountsInfo(self):
        data = (1, 'parity_allAccountsInfo', [])
        params = self._create_params(data)
        answer = await self._request_node(params)
        return answer

    async def _kill_account(self, address, phrase):
        '''
        Unlocks the given account for duration seconds.
        If duration is None then the account will remain unlocked indefinitely.
        Returns boolean as to whether the account was successfully unlocked.
        :param address: (address,passphrase)
        :param phrase: (address,passphrase)
        :return:
        (code,Boolean)
        '''
        data = [self.passphrase, phrase]
        for item in data:
            body = (1, 'parity_killAccount', [address, item])
            params = self._create_params(body)
            try:
                answer = await self._request_node(params)
            except Exception as msg:
                pass

        return None

    async def _unlock_account(self, body):
        '''
        Unlocks the given account for duration seconds.
        If duration is None then the account will remain unlocked indefinitely.
        Returns boolean as to whether the account was successfully unlocked.
        :param body: (address,passphrase)
        :return:
        (code,mode,Boolean)
        (200,'Ok', logic)
        '''
        (address, passphrase) = body
        try:
            answer = self.web3.parity.personal.unlockAccount(
                address, passphrase)
        except Exception as msg:
            return (None, 'Account is lock', str(msg))
        return (200, 'OK', answer)

    # Helper for Request for crypto Nodes Etherium
    async def get_transaction(self, hash):
        return self.web3.eth.getTransactionFromBlock(hash)

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
        (address, value, gas) = body

        nonce = self._take_nonce(address)
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

    async def __generate_phase(self):
        body = (1, 'parity_generateSecretPhrase', [])
        params = self._create_params(body)
        (code, mode, data) = await self._request_node(params)

        body = (1, 'parity_phraseToAddress', [data['result']])
        params = self._create_params(body)
        (code, mode, param) = await self._request_node(params)

        answer = [param['result'], data['result']]
        return (code, mode, answer)

    async def _request_node(self, params):
        '''
        send request for aiohttp and fetch answer data in CryptoNodes ETH
        :param params: create with method _create_params
        :return:
        (code,data['result'])
        (200,'Ok')
        '''
        answer = await send_request_aiohttp(params)
        return answer

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
        return self.web3.eth.getTransactionCount(address)

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
