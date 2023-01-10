#Import necessary libraries
import random
import secrets
import hashlib
from eth_account.messages import encode_defunct
import streamlit as st
import datetime
import time
import requests

# define function create_message.
@st.cache(allow_output_mutation=True,ttl=60)
def create_message():
    seed1 = str(random.random())
    seed2 = secrets.token_hex()
    seed3 = hashlib.sha256((seed1+seed2).encode()).hexdigest()
    expired_time = datetime.datetime.fromtimestamp(time.time() + 60).strftime("%Y-%m-%d %H:%M:%S")
    return seed3,expired_time

# define function to create signature
def create_signature(w3,account,message):
    signature = w3.eth.sign(account, text = message)
    return signature

# define function to recover and verify the account address
def signature_to_account(w3,message,signature):   
    recovered_address = w3.eth.account.recover_message(encode_defunct(text = message), signature=signature)
    return recovered_address

#define function to get user fingerprint info
def get_user_hash():
    ip_address = requests.get("https://api.ipify.org").text
    user_agent = requests.get("https://httpbin.org/user-agent").json()["user-agent"]
    user_hash = hashlib.sha256((ip_address+user_agent).encode()).hexdigest()
    return user_hash
