from web3 import Web3
import json
from dotenv import load_dotenv
import os

load_dotenv()
# Connect to Binance Smart Chain using POKT RPC node
pokt_url = os.getenv('pokt_url')

web3 = Web3(Web3.HTTPProvider(pokt_url))

# Check porkt_url is connected to bsc network
connected = web3.isConnected()
print(f"Connected to Binance Smart Chain: {connected}")

# Address of pancakeswap factory
pancakeswap_factory_address = '0xcA143Ce32Fe78f1f7019d7d551a6402fC5350c73'
# Address of pancakeswap router
pancakeswap_router_address = '0x10ED43C718714eb63d5aA57B78B54704E256024E'

# load pancakeswap_factory_abi
with open('pancakeswap_factory_abi.json') as f:
    factory_abi = json.load(f)
# load pancakeswap_pair_abi
with open('pancakeswap_pair_abi.json') as f:
    pair_abi = json.load(f)


def get_wbnb_price():
    try:
        # Get the pair address of WBNB
        factory_contract = web3.eth.contract(address=pancakeswap_factory_address, abi=factory_abi)
        wbnb_address = web3.toChecksumAddress('0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c')
        busd_address = web3.toChecksumAddress('0xe9e7CEA3DedcA5984780Bafc599bD69ADd087D56')
        wbnb_address = factory_contract.functions.getPair(wbnb_address, busd_address).call()

        # Get the contract instance of the WBNB pair
        pair_contract = web3.eth.contract(address=wbnb_address, abi=pair_abi)

        # Get the reserves of WBNB and BUSD from the pair contract
        reserves = pair_contract.functions.getReserves().call()
        wbnb_reserve, busd_reserve = reserves[0], reserves[1]

        # Calculate the WBNB price in BUSD
        wbnb_price = busd_reserve / wbnb_reserve

        return wbnb_price
    except Exception as e:
        print("Error retrieving WBNB price:", str(e))
        return None

# Get the price of WBNB
wbnb_price = get_wbnb_price()

# Print the price of WBNB
if wbnb_price is not None:
    print(f"The price of WBNB is {wbnb_price:.2f} BUSD")
else:
    print("Failed to fetch WBNB price.")
