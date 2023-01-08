import streamlit as st
from Modules.Verify import create_message,signature_to_account

message = create_message()
st.text_input(label = "Message to be signed", value = message,key="message",disabled=True)
#  check access

if st.button("Verify your idendity"):
    st.write("User Information")
    st.write("Your access: " + str(access))
    st.write("Activating account: " + w3.eth.default_account)
    st.write("Block number: " + str(w3.eth.get_block_number()))
    st.write("Chain ID: " + str(w3.eth.chain_id))
    st.write("Balance: " + str(w3.eth.get_balance(w3.eth.default_account))+" Wei")        
    st.write("Node Mining: " + str(w3.eth.mining))

# Send transaction
from_address = st.text_input("From account", key= "TX_from")

#To address
to_address = st.text_input("To account", key= "TX_To")

#Get the current balances for both account
st.write("From account balance: " + str(w3.eth.get_balance(from_address)))
st.write("To account balance: " + str(w3.eth.get_balance(to_address)))

#transaction detail
amount = int(st.number_input("the amount by Wei you want to send"))
gas_price = w3.eth.gasPrice

txn_params = {
    "from": from_address,
    "to": to_address,
    "gas": 100000,
    "gasPrice": gas_price,
    "value": amount,
    "nonce": w3.eth.get_transaction_count(from_address)
}

# transaction button
if st.button("Conduct transaction"):
    #Signed_txn
    #signed_txn = w3.eth.account.sign_transaction(txn_params,"3a4b5aa67fc8ab35f2be624e13cdf91d956ba7a734242d8c1a7d97f90f3c67ad")
    #Send the transaction
    #txn_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    txn_hash = w3.eth.send_transaction(txn_params)
    txn_receipt = w3.eth.waitForTransactionReceipt(txn_hash)
    st.write(txn_receipt)
    #after transaction balance
    st.write("From account balance: " + str(w3.eth.get_balance(from_address)))
    st.write("To account balance: " + str(w3.eth.get_balance(to_address)))

message = st.text_input("Message to be sign")
#Sign message
if st.button("Sign Message"):

    signature = NFT_contract.functions.sign(message).transact(txn_params)
    st.write(signature)