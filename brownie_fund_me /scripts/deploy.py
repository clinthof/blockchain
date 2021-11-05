from brownie import FundMe, MockV3Aggregator, network, config
from scripts.helper_scripts import (
    deploy_mocks,
    get_account,
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
)


# deploy to testnet
def deploy_fund_me():
    account = get_account()
    # pass priceFeed address to FundMe contract constructor; tell brownie to verify contract
    # if on persistent, live network chain (e.g., rinkeby): use associated address
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        price_feed_address = config["networks"][network.show_active()][
            "eth_usd_price_feed"
        ]
    # otherwise, if dev (i.e., spinning ganache or listen@RPC), use mock(s)
    else:
        deploy_mocks()
        price_feed_address = MockV3Aggregator[-1].address

    fund_me = FundMe.deploy(
        price_feed_address,
        {"from": account},
        publish_source=config["networks"][network.show_active()].get(
            "verify"
        ),  # .get in case verify absent
    )
    print(f"Contract deployed to {fund_me.address}")


def main():
    deploy_fund_me()
