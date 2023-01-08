from .ConnectDB import *
from datetime import datetime
import pytz
 
 ######Intert temporary verify info into Database########
def verifier_db(user_hash):

    # Convert to NewYork Time
    ny_timezone = pytz.timezone("America/New_York")
    ny_time = datetime.now(ny_timezone)
    Newyork_time = str(ny_time).split(' ')[0]
    # prepare table_name as today's date
    verifier_table_name = "_" + Newyork_time.replace('-', '_') + '_verifier'
    # Create table if not esists,
    cur.execute(
    "CREATE TABLE IF NOT EXISTS %s (create_time TIMESTAMPTZ, user_hash TEXT, expired_time TIMESTAMPTZ);" %verifier_table_name)
    # excute SQL command
    con.commit()
    # Insert all data to database and excute.  
    cur.execute("INSERT INTO {} (create_time,user_hash, expired_time) VALUES (%s,%s, %s)".format(verifier_table_name),
    (ny_time, user_hash, ny_time+600))
    # excute query
    con.commit()