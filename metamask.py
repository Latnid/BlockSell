from web3 import Web3

# Connect to Metamask
provider = Web3.WebsocketProvider('ws://127.0.0.1:7545')
w3 = Web3(provider)

# Ask the user to sign a message
message = 'Hello from Toptal!'
signed_message = w3.eth.sign(w3.eth.coinbase, message)

print(signed_message)