import streamlit as st


def Content_page1(w3,NFT_contract,CPC):

    if st.button("Verify your idendity"):
        st.write("User Information")
        st.write("Activating account: " + w3.eth.default_account)
        st.write("Block number: " + str(w3.eth.get_block_number()))
        st.write("Chain ID: " + str(w3.eth.chain_id))
        st.write("Balance: " + str(w3.eth.get_balance(w3.eth.default_account))+" Wei")        
        st.write("Node Mining: " + str(w3.eth.mining))
    
    # Send transaction
    from_address = st.text_input("From account", key= "TX_from",value= w3.eth.default_account)

    #To address
    to_address = st.text_input("To account", key= "TX_To",value=w3.eth.default_account)

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

        signature = NFT_contract.functions.sign(message).transact(txn_params).hex()
        st.write(signature)

    st.title("Create Artwork")
    #Create Arework
    owner_of_NFT = st.text_input("The first owner of this NFT you want to assigned")
    art_name = st.text_input("Name of Artwork")
    artist_name = st.text_input("The artist name")
    appraisal = int(st.number_input("Artwork price(Wei)"))
    artwork_URI = st.text_input("Artwork URI")

    if st.button("Create Artwork"):
        if w3.eth.default_account != w3.eth.coinbase:
            st.write("Only the contract owner can Create Artwork!")
        else:
            token_ID = NFT_contract.functions.CreatArtwork(owner_of_NFT,art_name,artist_name,appraisal,artwork_URI).transact({
            'from': w3.eth.default_account, # Ethereum address of the sender
            'to':CPC,
            'gas': 1000000, # Gas limit
            'gasPrice': w3.toWei('20', 'gwei'), # Gas price in wei
            'value': 0, # value must be 0 as the function is not payable
            
            })
            receipt = w3.eth.waitForTransactionReceipt(token_ID)
            st.write("Receipt is ready. Here it is:")
            st.write(dict(receipt))

    #Buy Artwork
    st.title("Buy Artwork")
    artwork_tokenID = int(st.number_input("Artwork tokenID",))
    buyer_address = st.text_input("buyer account")
    buyer_offer = int(st.number_input("Price offer"))
    if st.button("Buy Artwork"):
        
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