from Modules.Web3Connect import w3_contract
from Modules.ConnectDB import *
from dotenv import load_dotenv
from Modules.Verify import get_user_hash
from Modules.DBer import login_status
from Modules.SVIPfeatures import SVIP_page1
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
    user_hash_first4 = user_hash[:4]
    user_hash_last4 = user_hash[-4:]
    md_user_hash = f"User hash:\n{user_hash_first4}******************{user_hash_last4}"
    st.sidebar.markdown(md_user_hash)

    #create web3 instance and load contract
    RPC = os.getenv("WEB3_PROVIDER_URI2")
    CPC = os.getenv("SMART_CONTRACT_ADDRESS2")

    #Connect to Web3 and contract
    w3, NFT_contract = w3_contract(RPC,CPC) 

    #Check login_status
    user_login_status = login_status(cur,user_hash)
    if user_login_status == False:
        st.sidebar.markdown("You haven't login")
    if user_login_status == True:
        st.sidebar.markdown("Valid user")

        #Verify NFT owner access
        NFT_owner = NFT_contract.functions.isNFTOwner(w3.eth.default_account).call({
            'from': w3.eth.default_account,
            'to':CPC,
            })
        
        if NFT_owner == True:
            st.sidebar.markdown("You have NFT owner access")
        
        #Verify SVIP access
        SVIP_NFT_owner = NFT_contract.functions.isNFTOwnerVIP(7).call({
            'from': w3.eth.default_account,
            'to':CPC,
            })
        if SVIP_NFT_owner == True:
            st.sidebar.subheader("You have SVIP access")
            if st.sidebar.button("Open SVIP feature"):
                SVIP_page1(w3,NFT_contract,CPC)
    

    #return all required variables
    return w3,NFT_contract,con,cur,user_hash,user_login_status,RPC,CPC