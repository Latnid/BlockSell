import os
from Modules.Web3Connect import w3_contract
from Modules.Verify import create_message,signature_to_account,user_hash
from Modules.DBer import verifier_db
from pathlib import Path
from dotenv import load_dotenv
from eth_account.messages import encode_defunct
import streamlit as st
from Modules.ConnectDB import *

#load env file
load_dotenv()

# Connect DataBase
con,cur = connect_data_base()

#create web3 instance and load contract
RPC = os.getenv("WEB3_PROVIDER_URI2")
CPC = os.getenv("SMART_CONTRACT_ADDRESS2")

w3, NFT_contract = w3_contract(RPC,CPC)

#load all the accounts from database
database_address_list = w3.eth.accounts

#show the message required to be sign
message,expired_time = create_message()
st.text_input(label = "Message to be signed", value = message,key="message",disabled=True)

user_signature = st.text_input(f'You have 30 seconds to input your signature, Message refresh time: {expired_time}')
if st.button("Login"):
    if len(user_signature) != 132:
        st.write("login fail(1)")
    elif (user_signature.startswith("0x") or user_signature.startswith("0X")) == False:
        st.write("login fail(2)")
    elif str.isalnum == False:
        st.write("login fail(3)")
    else:
        try: 
            recover_address = signature_to_account(w3=w3,message=message, signature=user_signature)
        except Exception as e:
            st.write(f"Login failed(4)-{e}")
        else:
            for database_address in database_address_list:
                if recover_address == database_address:
                    st.write("Welcome abort")
                    #Set User default address
                    w3.eth.default_account = recover_address
                    #Input verify hash to Database
                    user_hash = user_hash()
                    verifier_db(user_hash)
  
                else:
                    st.write("You don't own this account")

@st.cache
def greet(name):
    return f"Hello, {name}!"

name = st.text_input("Enter your name")
st.write(greet(name))