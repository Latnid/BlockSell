import os
from Modules.Verify import user_hash
from Modules.DBer import login_status
from pathlib import Path
import streamlit as st
from Modules.ConnectDB import *
from Pages.Login import Login

#Set page config
st.set_page_config(
    page_title="Welcome to BlockSell",
    page_icon="👋",
)

#Read user hash info
user_hash=user_hash()
md_user_hash = f"User hash:\n{user_hash}"
st.sidebar.markdown(md_user_hash)

# Connect DataBase
con,cur = connect_data_base()

#Check login_status
login_status = login_status(cur,user_hash)
if login_status == False:
    st.sidebar.markdown("You haven't login")
if login_status == True:
    st.sidebar.markdown("Valid user")

#Load base on login status:
if login_status == True:
    exec(Path("./Pages/Content.py"))
else:
    Login(con,cur)