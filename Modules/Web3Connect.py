from web3 import Web3
import streamlit as st
from pathlib import Path
import json
import os

@st.cache(allow_output_mutation=True)
def w3_contract(RPC,CPC):
    '''
    RPC type is string
    RPC = 'ws://localhost:7545'
    CPC type is string
    CPC = "SMART_CONTRACT_ADDRESSS2"
    '''
    w3 = Web3(Web3.WebsocketProvider(RPC))

    # load contract
    with open(Path("./Contracts/NFT_abi.json")) as abi:
        abi = json.load(abi)

    contract_address = os.getenv(CPC)

    contract = w3.eth.contract(
        address= contract_address,
        abi= abi
    )

    return w3,contract



