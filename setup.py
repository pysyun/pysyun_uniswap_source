from setuptools import setup

setup(
    name='pysyun_uniswap_source',
    version='1.1.3',
    author='Immortal Tapok',
    author_email='immortaltapok@lineardev.net',
    py_modules=['pysyun_uniswap_source.uniswap_source', 'pysyun_uniswap_source.abi.uniswap_abi'],
    install_requires=['web3', 'requests', 'dotenv']
)
