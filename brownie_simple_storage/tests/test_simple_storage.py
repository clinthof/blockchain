from brownie import SimpleStorage, accounts


def test_deploy():
    # arrange
    account = accounts[0]
    # act
    simple_storage = SimpleStorage.deploy({"from": account})
    start_val = simple_storage.retrieve()
    expected = 0
    # assert
    assert start_val == expected


def test_update():
    # arrange
    account = accounts[0]
    simple_storage = SimpleStorage.deploy({"from": account})
    # act
    expected = 15
    simple_storage.store(15, {"from": account})
    # assert
    assert simple_storage.retrieve() == expected
