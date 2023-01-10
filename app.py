import os
from Modules.Verify import get_user_hash
from Modules.Content import Content_page1
from Modules.DBer import login_status
from pathlib import Path
import streamlit as st
from Modules.ConnectDB import *
from Modules.Web3Connect import w3_contract
from Modules.Login import Login

#Set page config
st.set_page_config(
    page_title="Welcome to BlockSell",
    page_icon="👋",
)

#Read user hash info
user_hash=get_user_hash()
md_user_hash = f"User hash:\n{user_hash}"
st.sidebar.markdown(md_user_hash)

# Connect DataBase
con,cur = connect_data_base()

#create web3 instance and load contract
RPC = os.getenv("WEB3_PROVIDER_URI2")
CPC = os.getenv("SMART_CONTRACT_ADDRESS2")

#Connect to Web3 and contract
w3, NFT_contract = w3_contract(RPC,CPC)

#Check login_status
#login_status = False
login_status = login_status(cur,user_hash)

def login_status_sidebar():
    if login_status == False:
        st.sidebar.markdown("You haven't login")
    if login_status == True:
        st.sidebar.markdown("Valid user")

login_status_sidebar()

#Load base on login status:
if login_status == True:
    Content_page1(w3,NFT_contract)
else:
    Login(con,cur,user_hash)