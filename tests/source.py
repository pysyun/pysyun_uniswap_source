from pysyun_uniswap_source.uniswap_source import UniswapV2PairsSource

pairs = UniswapV2PairsSource(
    "https://bsc-dataseed1.binance.org:443",
    "0xcA143Ce32Fe78f1f7019d7d551a6402fC5350c73",
    50).process([])
print(pairs)
