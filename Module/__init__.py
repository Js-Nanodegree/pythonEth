import json
import asyncio

from web3 import Web3

from utils import send_request_aiohttp

abi = json.loads(
    '[{"constant":true,"inputs":[],"name":"mintingFinished","outputs":[{"name":"","type":"bool"}],"payable":false,"type":"function"},{"constant":true,"inputs":[],"name":"name","outputs":[{"name":"","type":"string"}],"payable":false,"type":"function"},{"constant":false,"inputs":[{"name":"_spender","type":"address"},{"name":"_value","type":"uint256"}],"name":"approve","outputs":[],"payable":false,"type":"function"},{"constant":true,"inputs":[],"name":"totalSupply","outputs":[{"name":"","type":"uint256"}],"payable":false,"type":"function"},{"constant":false,"inputs":[{"name":"_from","type":"address"},{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"transferFrom","outputs":[],"payable":false,"type":"function"},{"constant":true,"inputs":[],"name":"decimals","outputs":[{"name":"","type":"uint256"}],"payable":false,"type":"function"},{"constant":false,"inputs":[],"name":"unpause","outputs":[{"name":"","type":"bool"}],"payable":false,"type":"function"},{"constant":false,"inputs":[{"name":"_to","type":"address"},{"name":"_amount","type":"uint256"}],"name":"mint","outputs":[{"name":"","type":"bool"}],"payable":false,"type":"function"},{"constant":true,"inputs":[],"name":"paused","outputs":[{"name":"","type":"bool"}],"payable":false,"type":"function"},{"constant":true,"inputs":[{"name":"_owner","type":"address"}],"name":"balanceOf","outputs":[{"name":"balance","type":"uint256"}],"payable":false,"type":"function"},{"constant":false,"inputs":[],"name":"finishMinting","outputs":[{"name":"","type":"bool"}],"payable":false,"type":"function"},{"constant":false,"inputs":[],"name":"pause","outputs":[{"name":"","type":"bool"}],"payable":false,"type":"function"},{"constant":true,"inputs":[],"name":"owner","outputs":[{"name":"","type":"address"}],"payable":false,"type":"function"},{"constant":true,"inputs":[],"name":"symbol","outputs":[{"name":"","type":"string"}],"payable":false,"type":"function"},{"constant":false,"inputs":[{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"transfer","outputs":[],"payable":false,"type":"function"},{"constant":false,"inputs":[{"name":"_to","type":"address"},{"name":"_amount","type":"uint256"},{"name":"_releaseTime","type":"uint256"}],"name":"mintTimelocked","outputs":[{"name":"","type":"address"}],"payable":false,"type":"function"},{"constant":true,"inputs":[{"name":"_owner","type":"address"},{"name":"_spender","type":"address"}],"name":"allowance","outputs":[{"name":"remaining","type":"uint256"}],"payable":false,"type":"function"},{"constant":false,"inputs":[{"name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"payable":false,"type":"function"},{"anonymous":false,"inputs":[{"indexed":true,"name":"to","type":"address"},{"indexed":false,"name":"value","type":"uint256"}],"name":"Mint","type":"event"},{"anonymous":false,"inputs":[],"name":"MintFinished","type":"event"},{"anonymous":false,"inputs":[],"name":"Pause","type":"event"},{"anonymous":false,"inputs":[],"name":"Unpause","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"owner","type":"address"},{"indexed":true,"name":"spender","type":"address"},{"indexed":false,"name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"from","type":"address"},{"indexed":true,"name":"to","type":"address"},{"indexed":false,"name":"value","type":"uint256"}],"name":"Transfer","type":"event"}]')


class ETH:
    def __init__(self, smart_contract, hw, host, key, currency_id, mnemonc, passphrase,send_request_aiohttp,log_dir):
        self.web3 = Web3(Web3.HTTPProvider(host))  # ADD web3 interface init state
        self.send_aiohttp = send_request_aiohttp
        self.log_dir = log_dir
        self._loop = asyncio.get_event_loop()  # ADD asyncio loop
        self.smart_contract = smart_contract  # TODO ADD smart contract USDT take in config
        self._key = key  # TODO ADD key hash for raw transaction take in config
        self.passphrase = passphrase  # TODO ADD key passphrase for create address take in config default ("123123")
        self._host = host  # uri ETH address node
        self._password_wallet = passphrase  # key phrase for create and transaction
        self._hot_wallet = hw  # initial hotwallet address
        self._currency_id = currency_id  # current id cryptonodes

    """
        PUBLIC FUNCTION FOR CRYPTONODES 
    """
    async def get_new_address(self,remote_id):
        """
        this method create Eth Address and set Label for address
        :param label: (phrase, label) => (Take in Config password phase, Remote ID)
        :return:
        (current_contract ,address_wallet, label_wallet)
        (200, '0x967a9C9f42ccC2891Cf89731E6D4F1279C0dB9d7', 'HW')
        """
        # create address with new personal client parity account
        address = await self._create_account()
        if address is None:
            return None
        # unlock created account
        body = (address, self.passphrase)
        code = await self._unlock_account(body)
        if code is not None:
            body = [self._check_sum_address(address), remote_id]
            (code,mode,data) = await self._parity_set_label(body)
            if code == 200:
                return  address

        data = await self._kill_address(address)
        return data

    async def get_balance(self,address):
        # request from ETH
        if self._currency_id ==4:
            ballance = await self._check_balance_eth(address)
            answer = await self._from_wei(ballance)
            return answer
        elif self._currency_id ==7:
            ballance = await self._check_balance_usdt(address)
            answer = await self._from_wei(ballance)
            return answer
        else:
            return None

    async def get_accounts(self,type='meta'):
        responce = {}
        resArray = []
        answer = await self._parity_accounts_info()
        if answer is None:
            return None
        try:
            data = answer['result']
        except:
            return None

        for (x, i) in data.items():
            if x != self._hot_wallet:
                if type == 'name':
                    responce[x] = i['name']
                if type == 'all':
                    resArray.append(x)
                else:
                    responce[x] = i['meta']

        if type=='all':
            return resArray
        else:
            return responce


    async def set_status_address(self, body):
        (address, key, value) = body
        body = (1, 'parity_setAccountMeta', [address, str(json.dumps({key: value}))])
        params = self._create_params(body)
        answer = await self.send_aiohttp(params)
        try:
            (code, mode, data) = answer
        except Exception as msg:
            return (None, 'Meta not install', str(msg))

        if code == 200:
            return answer
        else:
            return (None, 'Meta not install', data)

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

    """
        PRIVATE FUNCTION FOR CRYPTONODES 
    """

    async def _parity_accounts_info(self):
        body = (1, 'parity_allAccountsInfo', [])
        params = self._create_params(body)
        try:
            (code, mode, data) = await self.send_aiohttp(params)
        except Exception as msg:
            return None
        return data

    async def _check_balance_eth(self,address):
        try:
            ballance = self.web3.eth.getBalance(self._check_sum_address(address))
        except Exception as msg:
            return None
        return ballance

    async def _check_balance_usdt(self, address):
        contact = self._build_contract_usdt()
        try:
            ballance = contact.functions.balanceOf(self._check_sum_address(address)).call()
        except Exception as msg:
            return None
        return ballance

    async def _create_account(self):
        try:
            address = self.web3.parity.personal.newAccount(self.passphrase)
        except Exception as msg:
            return None
        return address

    async def _kill_address(self, address):
        body = (1, 'parity_killAccount', [address, self.passphrase])
        params = self._create_params(body)
        try:
            (code,mode,data) = await self.send_aiohttp(params)
        except Exception as msg:
        # TODO WRITE LOG ADDRESS
            return None
        return None

    async def _unlock_account(self, body):
        (address, passphrase) = body
        try:
            answer = self.web3.parity.personal.unlockAccount(address, passphrase)
        except Exception as msg:
            body = (1, 'parity_killAccount', [address, self.passphrase])
            (code, mode, data) = await  self._kill_address(body)
            return None
        return answer

    async def _parity_set_label(self, body):
        data = (1, 'parity_setAccountName', body)
        params = self._create_params(data)
        try:
            answer = await self.send_aiohttp(params)
        except Exception as msg:
            #   TODO CHECK THIS LOG FILE
            return (None, 'Label Not Set', str(msg))
        return answer

    async def _get_block(self):
        """
        function control ballance when he is synced
        :return:
        :rtype:
        """
        block = self.web3.eth.syncing
        if block is False:
            return False
        self.block = block['currentBlock']
        body = (None)
        data = await self.get_accounts(body)
        responce = []
        for x in data:
            ballance = await self.get_balance(x)
            if ballance == 0:
                responce.append({x:block['currentBlock']})

        self.ballance = responce
        print(block['highestBlock']-block['currentBlock'],block['currentBlock'],self.ballance )
        return True

    async def _create_transaction(self, body):
        """
        If the transaction specifies a data value but does not specify gas
        then the gas value will be populated using the estimateGas()
        function with an additional buffer of 100000 gas up to the gasLimit of the latest block.
        In the event that the value returned by estimateGas()
        method is greater than the gasLimit a ValueError will be raised.
        :param body: (address,value,gas)
        :return:
        Returns a transaction that’s been signed by the node’s private key, but not yet submitted.
        The signed tx can be submitted with Eth.sendRawTransaction`
        """
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

    async def _send_raw_transaction(self, transaction):
        """
        Returns a transaction that’s been signed by the node’s private key, but not yet submitted.
        The signed tx can be submitted with Eth.sendRawTransaction`
        Sends a signed and serialized transaction. Returns the transaction hash as a HexBytes object.
        :param transaction: form create raw transaction
        :return:
        HexBytes('0xe670ec64341771606e55d6b4ca35a1a6b75ee3d5145a99d05921026d1527331')
        """
        create_raw_transaction = self.web3.eth.account.sign_transaction(
            transaction, self.key)
        try:
            send_raw_transaction = self.web3.eth.sendRawTransaction(
                create_raw_transaction.rawTransaction)
        except Exception as msg:
            return (None, 'Transaction Fall', str(msg))

        return (200, 'Ok', send_raw_transaction)

    async def _parity_set_label(self, body):
        data = (1, 'parity_setAccountName', body)
        params = self._create_params(data)
        try:
            answer = await self.send_aiohttp(params)
        except Exception as msg:
            #   TODO CHECK THIS LOG FILE
            return (None, 'Label Not Set', str(msg))
        return answer

    """
        SERVICE FUNCTION FOR CRYPTONODES 
    """

    def _create_params(self, body):
        (key, method, args) = body
        params = {'method': 'POST', 'headers': {'content-type': 'application/json'},
                  'data': json.dumps({"jsonrpc": "2.0", "id": key, "method": method, "params": args}),
                  'url': self._host}
        return params

    def _build_contract_usdt(self):
        try:
            answer = self.web3.eth.contract(address=self.smart_contract, abi=abi)
        except Exception as msg:
            return None
        return answer

    async def __generate_phase(self):
        body = (1, 'parity_generateSecretPhrase', [])
        params = self._create_params(body)
        (code, mode, data) = await self.send_aiohttp(params)

        body = (1, 'parity_phraseToAddress', [data['result']])
        params = self._create_params(body)
        (code, mode, param) = await self.send_aiohttp(params)

        answer = [param['result'], data['result']]
        return (code, mode, answer)

    def _check_sum_address(self, address):
        try:
            answer = self.web3.toChecksumAddress(address)
        except Exception as msg:
            return None
        return answer

    async def _from_wei(self,ballance):
        if self._currency_id == 4:
            body = (ballance, 'ether')
        elif self._currency_id == 7:
            body = (ballance, 'mwei')
        else:
            return ballance

        try:
            answer = self.web3.fromWei(*body)
        except Exception as msg:
            return None
        return answer
