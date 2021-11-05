from brownie import network, config, accounts, MockV3Aggregator
from web3 import Web3

LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["deployment", "ganache-local"]

DECIMALS = 8
STARTING_PRICE = 200000000000


def get_account():
    return (
        accounts[0]
        if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS
        else accounts.add(config["wallets"]["from_key"])
    )


def deploy_mocks():
    print(f"\nActive network: {network.show_active()}\nDeploying mocks...\n")
    if len(MockV3Aggregator) <= 0:
        MockV3Aggregator.deploy(
            DECIMALS, STARTING_PRICE, {"from": get_account()}
        )  # M3VA constructor vars
    print("Mocks deployed.\n")
