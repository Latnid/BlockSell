from .ConnectDB import *
from datetime import datetime,timedelta
import pytz

 
 ######Intert temporary verify info into Database########
def login_success(con,cur,user_hash):

    # Convert to NewYork Time
    ny_timezone = pytz.timezone("America/New_York")
    ny_time = datetime.now(ny_timezone)
    expired_time = ny_time+timedelta(minutes=10)

    #Newyork_time = str(ny_time).split(' ')[0] #Only keep the date
    # prepare table_name
    verifier_table_name = "login_status"
    # Create table if not esists,
    cur.execute(
    "CREATE TABLE IF NOT EXISTS %s (create_time TIMESTAMPTZ, user_hash TEXT, expired_time TIMESTAMPTZ);" %verifier_table_name)
    # excute SQL command
    con.commit()
    # Insert all data to database and excute.  
    cur.execute("INSERT INTO {} (create_time,user_hash, expired_time) VALUES (%s,%s, %s)".format(verifier_table_name),
    (ny_time, user_hash, expired_time))
    # excute query
    con.commit()


def login_status(cur,user_hash):
    #Select the User_hash matched record
    cur.execute(
        "SELECT user_hash, expired_time FROM login_status WHERE user_hash = '{}' AND expired_time > NOW()".format(user_hash)
    )
    if cur.rowcount>0: #Found the user_hash in the table
        
        row = cur.fetchone()
        expired_time = row[1]
        ny_timezone = pytz.timezone("America/New_York")
        if expired_time > datetime.now(ny_timezone): #Login still valid
            user_login_status = True
            return user_login_status
        else:
            user_login_status = False # Login status is expired
            return user_login_status
    else:
        user_login_status = False
        return user_login_status

            
def logout(con,cur,user_hash):
    #Select the User_hash matched record
    cur.execute(
        "DELETE FROM login_status WHERE user_hash = %s",(user_hash,)
    )
    # excute query
    con.commit()
