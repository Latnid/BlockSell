from Modules.Basic import basic_load
from Modules.Content import Content_page1
from Modules.Login import Login

#Load all basic environment
w3,NFT_contract,con,cur,user_hash,user_login_status,RPC,CPC = basic_load()

#Load base on login status:
if user_login_status == True:
    Content_page1(w3,NFT_contract,CPC)
else:
    Login(w3,con,cur,user_hash)