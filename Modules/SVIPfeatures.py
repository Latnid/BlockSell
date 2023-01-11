import streamlit as st


def SVIP_page1(w3,NFT_contract,CPC):
    #Verify SVIP access
    SVIP_NFT_owner = NFT_contract.functions.isNFTOwnerVIP(7).call({
        'from': w3.eth.default_account,
        'to':CPC,
        })
    if SVIP_NFT_owner == True:
        st.title("Create Artwork")
        #Create Arework
        owner_of_NFT = st.text_input("The first owner of this NFT you want to assigned")
        art_name = st.text_input("Name of Artwork")
        artist_name = st.text_input("The artist name")
        appraisal = int(st.number_input("Artwork price(Wei)",step=1))
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