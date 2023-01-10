import streamlit as st
from Modules.Content import Content_page1
from Modules.Web3Connect import w3_contract
from Modules.ConnectDB import *
from dotenv import load_dotenv
from Modules.Web3Connect import w3_contract
from Modules.Login import Login
from Modules.Verify import get_user_hash
from Modules.DBer import login_status,logout
import os

#Read user hash info
user_hash=get_user_hash()
md_user_hash = f"User hash:\n{user_hash}"
st.sidebar.markdown(md_user_hash)

# Connect DataBase
con,cur = connect_data_base()

#load env file
load_dotenv()

#create web3 instance and load contract
RPC = os.getenv("WEB3_PROVIDER_URI2")
CPC = os.getenv("SMART_CONTRACT_ADDRESS2")

#Connect to Web3 and contract
w3, NFT_contract = w3_contract(RPC,CPC)

#Check login_status
#login_status = False
login_status = login_status(cur,user_hash)
if login_status == False:
    st.sidebar.markdown("You haven't login")
if login_status == True:
    st.sidebar.markdown("Valid user")

#Load base on login status:
if login_status == True:
    st.markdown("You already login")
    if st.button("Logout",key="logout_bt"):
        logout(con,cur,user_hash)
        st.write("Logout completed")
else:
    Login(con,cur,user_hash)


