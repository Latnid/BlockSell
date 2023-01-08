import os
import json
from web3 import Web3
from pathlib import Path
from dotenv import load_dotenv
from eth_account.messages import encode_defunct
import streamlit as st

load_dotenv()

# Connect to the Ethereum provider
w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER_URI2")))

# Set the message to be signed
message = "Hello from Toptal!"

# Get the current account
account = w3.eth.accounts[0]

# Sign the message using the current account
signature = w3.eth.account.sign_message(message, account)

# Print the signature
print(signature)
