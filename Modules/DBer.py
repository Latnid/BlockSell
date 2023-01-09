from .ConnectDB import *
from datetime import datetime,timedelta
import pytz
 
 ######Intert temporary verify info into Database########
def login_success(con,cur,user_hash):

    # Convert to NewYork Time
    ny_timezone = pytz.timezone("America/New_York")
    ny_time = datetime.now(ny_timezone)
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
    (ny_time, user_hash, ny_time+timedelta(minutes=10)))
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
            login_status = True
            return login_status
        else:
            login_status = False # Login status is expired
            return login_status
    else:
        login_status = False
        return login_status

            