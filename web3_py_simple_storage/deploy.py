from solcx import compile_standard, install_solc
import json
import os
from web3 import Web3
from dotenv import load_dotenv

load_dotenv()

with open("./SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()

install_solc("0.6.0")

# compile solidity
compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
            }
        },
    },
    solc_version="0.6.0",
)

with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)

# get bytecode
bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"][
    "bytecode"
]["object"]

# get abi (for deploying to ganache simulated chain)
abi = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]

# connect to rinkeby (or ganache if refactored)
w3 = Web3(
    Web3.HTTPProvider("https://rinkeby.infura.io/v3/b5bb9e2e711a451a975a472c61bb1680")
)  # RPC URL
chain_id = 4  # ETH Rinkeby testnet chain ID
rinkeby_addr = "0xc5b5bA3708269032d14AB676681845227E7Ca2E5"
private_key = os.getenv("PRIVATE_KEY")

# deploy SimpleStorage.sol contract to ganache local chain
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)

# get latest transaction
nonce = w3.eth.getTransactionCount(rinkeby_addr)

# DEPLOYING CONTRACT
print("deploying contract...")
# step 1: build transaction
transaction = SimpleStorage.constructor().buildTransaction(
    {"chainId": chain_id, "from": rinkeby_addr, "nonce": nonce}
)

# step 2: sign transaction
signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)

# step 3: send signed transaction
txn_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)

# wait for block confirmation(s) of txn hash
txn_receipt = w3.eth.wait_for_transaction_receipt(txn_hash)
print("deployed.")

# working with contract on chain (always need contract address and ABI)
# new interactable SS contract
simple_storage = w3.eth.contract(address=txn_receipt.contractAddress, abi=abi)

# call: simulate making the call and getting return value (no changes to state)
print(
    f"before state change to contract on local chain: {simple_storage.functions.retrieve().call()}"
)

# UPDATING COTNRACT
print("updating contract...")
# transact: make a state change (build and send a transaction)
store_txn = simple_storage.functions.store(15).buildTransaction(
    {
        "chainId": chain_id,
        "from": rinkeby_addr,
        "nonce": nonce + 1,
    }  # nonce was used previously; increment for new txn
)

signed_store_txn = w3.eth.account.sign_transaction(store_txn, private_key=private_key)
send_store_txn = w3.eth.send_raw_transaction(signed_store_txn.rawTransaction)
store_txn_receipt = w3.eth.wait_for_transaction_receipt(send_store_txn)
print("updated.")
# show state change to contract deployed on local chain
print(
    f"after state change to contract on local chain: {simple_storage.functions.retrieve().call()}"
)
