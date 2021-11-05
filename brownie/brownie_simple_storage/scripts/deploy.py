from brownie import accounts, config, SimpleStorage, network

# deployment logic
def deploy_simple_storage():
    # three ways to add accounts:
    # 1. ganache CLI local chain
    # account = accounts[0]
    # 2. working with testnet: encrypted command line (will require password to decrypt)
    # account = accounts.load("some-account-name-created-in-terminal")
    # 3. ENV vars and brownie config
    # account = accounts.add(config["wallets"]["from_key"])
    account = get_account()

    # deploy contract to chain (brownie will distinguish between call and txn); returns contract obj
    simple_storage = SimpleStorage.deploy({"from": account})
    stored_val = simple_storage.retrieve()
    print(f"before updating value: {stored_val}")

    # update contract (since txn, always add txn origin)
    txn = simple_storage.store(15, {"from": account})
    txn.wait(1)
    updated_stored_val = simple_storage.retrieve()
    print(f"after updating value: {updated_stored_val}")


# get account for deploying to testnet
def get_account():
    return (
        accounts[0]
        if network.show_active() == "deployment"
        else accounts.add(config["wallets"]["from_key"])
    )


def main():
    deploy_simple_storage()
