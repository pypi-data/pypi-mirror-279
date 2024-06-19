CODE = """# https://vyper-by-example.org/hello-world/
# @version ^0.3.0

greet: public(String[100])

@external
def __init__():
    self.greet = "Hello World"
"""
ABI = [
    {
        "stateMutability": "nonpayable",
        "type": "constructor",
        "inputs": [],
        "outputs": [],
    },
    {
        "stateMutability": "view",
        "type": "function",
        "name": "greet",
        "inputs": [],
        "outputs": [{"name": "", "type": "string"}],
    },
]
BYTECODE = "3461004c57600b6040527f48656c6c6f20576f726c64000000000000000000000000000000000000000000606052604080515f556020810151600155506100836100506000396100836000f35b5f80fd5f3560e01c63cfae3217811861007b573461007f576020806040528060400160205f54015f81601f0160051c6005811161007f57801561004f57905b80548160051b85015260010181811861003b575b5050508051806020830101601f825f03163682375050601f19601f825160200101169050810190506040f35b5f5ffd5b5f80fd8418838000a16576797065728300030a0012"

from web3 import Web3, EthereumTesterProvider


w3 = Web3(EthereumTesterProvider())

# provide `constructor` args if appropriate:
deploy = w3.eth.contract(abi=ABI, bytecode=BYTECODE).constructor().transact()
contract_address = w3.eth.get_transaction_receipt(deploy)["contractAddress"]
contract = w3.eth.contract(address=contract_address, abi=ABI)

# result = contract.functions.exampleFunction().call()
