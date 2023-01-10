from Modules.Web3Connect import w3_contract
from Modules.ConnectDB import *
from dotenv import load_dotenv
from Modules.Login import Login
from Modules.Verify import get_user_hash
from Modules.DBer import login_status
import os
import streamlit as st

def basic_load():
    # Connect DataBase
    con,cur = connect_data_base()

    #load env file
    load_dotenv()

    #Set page config
    st.set_page_config(
    page_title="Welcome to BlockSell",
    page_icon="👋",
)
    #Read user hash info
    user_hash=get_user_hash()
    md_user_hash = f"User hash:\n{user_hash}"
    st.sidebar.markdown(md_user_hash)

    #Check login_status
    user_login_status = login_status(cur,user_hash)
    if user_login_status == False:
        st.sidebar.markdown("You haven't login")
    if user_login_status == True:
        st.sidebar.markdown("Valid user")

    #create web3 instance and load contract
    RPC = os.getenv("WEB3_PROVIDER_URI2")
    CPC = os.getenv("SMART_CONTRACT_ADDRESS2")

    #Connect to Web3 and contract
    w3, NFT_contract = w3_contract(RPC,CPC)



    #return all required variables
    return w3,NFT_contract,con,cur,user_hash,user_login_status