import time
import json
from web3 import Web3
from abi.uniswap_abi import UniswapPairABI

class UniswapV2Source:
    def __init__(self, uniswap_address, blockchain_settings):
        self.uniswap_address = uniswap_address
        self.blockchain_settings = blockchain_settings
        self.web3 = Web3(Web3.HTTPProvider(blockchain_settings))
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
