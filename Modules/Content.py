import streamlit as st
from Modules.SVIPfeatures import SVIP_page1


def Content_page1(w3,NFT_contract,CPC):

    st.title("Chain Info")
    st.write("User Information")
    st.write("Activating account: " + w3.eth.default_account)
    st.write("Block number: " + str(w3.eth.get_block_number()))
    st.write("Chain ID: " + str(w3.eth.chain_id))
    st.write("Balance: " + str(w3.eth.get_balance(w3.eth.default_account))+" Wei")        
    st.write("Node Mining: " + str(w3.eth.mining))
    
    st.title("Fund transfer")
    # Send transaction
    from_address = st.text_input("From account", key= "TX_from",value= w3.eth.default_account)

    #To address
    to_address = st.text_input("To account", key= "TX_To",value=w3.eth.default_account)

    #Get the current balances for both account
    st.write("From account balance: " + str(w3.eth.get_balance(from_address)))
    st.write("To account balance: " + str(w3.eth.get_balance(to_address)))

    #transaction detail
    amount = int(st.number_input("the amount by Wei you want to send",step=1))
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

        signature = NFT_contract.functions.sign(message).transact(txn_params).hex()
        st.write(signature)

    #Buy Artwork
    st.title("Buy Artwork")
    artwork_tokenID = int(st.number_input("Artwork tokenID",step=1))
    NFT_info = NFT_contract.functions.artCollection(artwork_tokenID).call({
        'from': w3.eth.default_account,
        'to':CPC,
        })
    st.write("NFT information:" + str(NFT_info))
    buyer_address = w3.eth.default_account
    buyer_offer = int(st.number_input("Price offer",step=1))
    if st.button("Buy Artwork"):
        
    #     txn_receipt_buy = NFT_contract.functions.buy(artwork_tokenID).transact({
    #     'from': buyer_address, # Ethereum address of the sender
    #     'to':CPC,
    #     'gas': 1000000, # Gas limit
    #     'gasPrice': w3.toWei('20', 'gwei'), # Gas price in wei
    #     'value': buyer_offer, # value must be 0 as the function is not payable
        
    # })
    #     receipt = w3.eth.waitForTransactionReceipt(txn_receipt_buy)
    #     st.write("Receipt is ready. Here it is:")
    #     st.write(dict(receipt))

        try:
            txn_receipt_buy = NFT_contract.functions.buy(artwork_tokenID).transact({
            'from': buyer_address, # Ethereum address of the sender
            'to':CPC,
            'gas': 1000000, # Gas limit
            'gasPrice': w3.toWei('20', 'gwei'), # Gas price in wei
            'value': buyer_offer, # value must be 0 as the function is not payable
            
            })
            receipt = w3.eth.waitForTransactionReceipt(txn_receipt_buy)
            st.write("Receipt is ready. Here it is:")
            st.write(dict(receipt))
            #Enable automatic refresh
            st.experimental_rerun()
        except ValueError as e:
            
            st.write("An error occurre,check price,or you may already have the NFT onhand")

    #Verify SVIP access
    SVIP_NFT_owner = NFT_contract.functions.isNFTOwnerVIP(7).call({
        'from': w3.eth.default_account,
        'to':CPC,
        })
    if SVIP_NFT_owner == True:
        SVIP_page1(w3,NFT_contract,CPC)
        
