// SPDX-License-Identifier: MIT

pragma solidity ^0.6.0;

contract SimpleStorage {
    uint256 num;

    struct People {
        uint256 num;
        string name;
    }

    People[] public people;
    mapping(string => uint256) public nameToNum;

    function store(uint256 _passedNum) public {
        num = _passedNum;
    }

    function retrieve() public view returns (uint256) {
        return num;
    }

    function addPerson(string memory _name, uint256 _num) public {
        people.push(People(_num, _name));
        nameToNum[_name] = _num;
    }
}
