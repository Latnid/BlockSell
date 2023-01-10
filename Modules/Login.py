from Modules.Verify import create_message,signature_to_account
from Modules.DBer import login_success
import streamlit as st
from Modules.ConnectDB import *


def Login(w3,con,cur,user_hash):

    #load all the accounts from database
    database_address_list = w3.eth.accounts

    #show the message required to be sign
    message,expired_time = create_message()
    st.text_input(label = "Message to be signed", value = message,key="message",disabled=True)

    user_signature = st.text_input(f'You have 60 seconds to input your signature, Message refresh time: {expired_time}')
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
                        st.write("Welcome aboard")
                        #Set User default address
                        w3.eth.default_account = recover_address
                        #Input verify hash to Database
                        #user_hash = get_user_hash()
                        login_success(con,cur,user_hash)
                        # Enable automatic refresh
                        st.experimental_rerun()
                    else:
                        pass
