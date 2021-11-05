# read from deployed rinkeby contract
from brownie import SimpleStorage, accounts, config


def read_contract():
    # always retrieves most recent deployment (address saved in build > 
    # deployments, ABI saved in build > contracts > respective JSON by brownie)
    simple_storage = SimpleStorage[-1]
    simple_storage.retrieve()


def main():
    read_contract()
