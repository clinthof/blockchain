from brownie import FundMe
from scripts.helper_scripts import *


def fund():
    fund_me = FundMe[-1]
    account = get_account()
    entrance_fee = fund_me.getEntranceFee()
    print(f"\nEntrance fee: {entrance_fee}\nFunding...\n")
    fund_me.fund({"from": account, "value": entrance_fee})


def withdraw():
    fund_me = FundMe[-1]
    account = get_account()
    print(f"\nWithdrawing from account {account}...\n")
    fund_me.withdraw({"from": account})


def main():
    fund()
    withdraw()
