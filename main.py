import requests
import os
import time
import json
from dotenv import load_dotenv
from tqdm import tqdm

from pysyun_uniswap_source.uniswap_source import UniswapV2PairsSource, UniswapV2ReservesSource

load_dotenv()

database_url = os.environ.get('STORAGE_TIMELINE_URI')
ethereum_rpc_uri = os.environ.get('ETHEREUM_RPC_URI')
uniswap_factory_contract_address = os.environ.get('UNISWAP_FACTORY_CONTRACT_ADDRESS')
last_pairs_count = int(os.environ.get('LAST_PAIRS_COUNT', 17))

progress_bar = tqdm(total=last_pairs_count, ncols=80)

pairs = UniswapV2PairsSource(
    ethereum_rpc_uri,
    uniswap_factory_contract_address,
    last_pairs_count).process([])

schema_name = f"{uniswap_factory_contract_address}.last-{last_pairs_count}-pair"


def create_schema():
    requests.post(database_url, json={
        "schema": schema_name
    })


create_schema()

for pair in pairs:

    reserves = UniswapV2ReservesSource(ethereum_rpc_uri, pair).process([])

    # Try to create the time-line
    requests.post(database_url, json={
        "schema": schema_name,
        "timeLine": pair
    })

    # Try to save the data item
    database_response = requests.put(database_url, json={
        "time": int(time.time()) * 1000,  # To milliseconds
        "value": json.dumps(reserves)
    }, params={
        'format': 'string',
        "schema": schema_name,
        "timeLine": pair
    })
    if database_response.text != '1':
        print(f"Storage.Timeline error: {database_response.text}")

        # Most likely, the schema does not exist
        create_schema()

    progress_bar.update(1)

    time.sleep(0.5)

progress_bar.close()
