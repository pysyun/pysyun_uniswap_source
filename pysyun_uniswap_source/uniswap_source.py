import time
import json
from web3 import Web3
from pysyun_uniswap_source.abi.uniswap_abi import UniswapPairABI
from pysyun_uniswap_source.abi.uniswap_factory_abi import UniswapFactoryAbi

class UniswapV2Source:
    def __init__(self, provider_settings, uniswap_address):
        self.uniswap_address = uniswap_address
        self.provider_settings = provider_settings
        self.web3 = Web3(Web3.HTTPProvider(provider_settings))
        self.pair_abi = UniswapPairABI.get()
        self.timeline = []

    def process(self):
        # Отримуємо дані пари Uniswap
        uniswap_pair = self.web3.eth.contract(address=self.uniswap_address, abi=self.pair_abi)

        # Отримуємо значення reserve0 і reserve1
        reserve0 = uniswap_pair.functions.getReserves().call()[0]
        reserve1 = uniswap_pair.functions.getReserves().call()[1]

        # Отримання поточної дати та часу
        current_time = time.time()

        # Створення результату у форматі JSON
        result = {
            "timestamp": current_time,
            "value": [reserve0, reserve1]
        }

        # Додавання результату до списку "timeline"
        self.timeline.append(result)

        # Повернення списку "timeline" у форматі JSON
        return json.dumps(self.timeline)

class UniswapV2PairsSource:

    def __init__(self, provider_settings, pairs_number=1000):
        self.max_pairs_num = 252434
        self.pairs_number = pairs_number
        self.provider_settings = provider_settings
        self.web3 = Web3(Web3.HTTPProvider(provider_settings))
        self.pair_abi = UniswapFactoryAbi.get()

    def process(self):
        contract = self.web3.eth.contract(address="0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f", abi=UniswapFactoryAbi.get())
        result = []

        for i in range(self.max_pairs_num, self.max_pairs_num - self.pairs_number, -1):
            address = contract.functions.allPairs(i).call()
            result.append(address)

        return result


