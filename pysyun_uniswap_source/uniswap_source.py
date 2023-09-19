import json
import time

from web3 import Web3
from eth_utils import to_checksum_address
from pysyun_uniswap_source.abi.uniswap_abi import UniswapPairABI
from pysyun_uniswap_source.abi.uniswap_factory_abi import UniswapFactoryAbi


class UniswapV2ReservesSource:

    def __init__(self, provider_settings, uniswap_pair_address):
        self.provider_settings = provider_settings
        self.uniswap_pair_address = uniswap_pair_address

    def process(self, _):
        __web3 = Web3(Web3.HTTPProvider(self.provider_settings))
        uniswap_pair = __web3.eth.contract(address=self.uniswap_pair_address, abi=UniswapPairABI.get())

        reserve0 = uniswap_pair.functions.getReserves().call()[0]
        reserve1 = uniswap_pair.functions.getReserves().call()[1]

        result = {
            "time": int(time.time()) * 1000,  # To milliseconds
            "value": json.dumps({
                "r": [reserve0, reserve1]
            })
        }

        return [result]


class UniswapV2PairsSource:

    def __init__(self,
                 provider_settings,
                 uniswap_factory_address,
                 last_pairs_count=1000):
        self.provider_settings = provider_settings
        self.uniswap_factory_address = to_checksum_address(uniswap_factory_address)
        self.last_pairs_count = last_pairs_count
        self.web3 = Web3(Web3.HTTPProvider(provider_settings))
        self.pair_abi = UniswapFactoryAbi.get()

    def process(self, _):
        contract = self.web3.eth.contract(address=self.uniswap_factory_address, abi=UniswapFactoryAbi.get())

        current_pairs_count = contract.functions.allPairsLength().call()

        result = []
        for i in range(current_pairs_count - self.last_pairs_count - 1, current_pairs_count - 1):
            address = contract.functions.allPairs(i).call()
            result.append(address)

        return result
