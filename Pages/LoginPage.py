import streamlit as st
from Modules.ConnectDB import *
from Modules.Login import Login
from Modules.DBer import logout
import os
from Modules.Basic import basic_load

#Load all basic environment
w3,NFT_contract,con,cur,user_hash,user_login_status,RPC,CPC = basic_load()

#Load base on login status:
if user_login_status == True:
    st.markdown("You already login")
    if st.button("Logout",key="logout_bt"):
        logout(con,cur,user_hash)
        st.write("Logout completed")                        
        # Enable automatic refresh
        st.experimental_rerun()
else:
    Login(w3,con,cur,user_hash)


