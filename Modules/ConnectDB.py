import os
from dotenv import load_dotenv
import psycopg2
import datetime


# Load and assign variables.
load_dotenv()
SQL_DB = os.getenv('SQL_DB')
SQL_USER = os.getenv("SQL_USER")
SQL_PASSWORD = os.getenv("SQL_PASSWORD")
SQL_HOST = os.getenv("SQL_HOST")

def connect_data_base(database = SQL_DB, user = SQL_USER, password=SQL_PASSWORD, host=SQL_HOST):
    con = psycopg2.connect(database = SQL_DB, user = SQL_USER, password=SQL_PASSWORD, host=SQL_HOST)
    cur = con.cursor()
    cur.execute('SELECT version()')
    version = cur.fetchone()[0]
    print(f"DataBase Connected!\nVersion: {version}")
    return con, cur

# def connect_data_base(database = SQL_DB, user = SQL_USER, password=SQL_PASSWORD, host=SQL_HOST):
#     # Check database connection,if not connected, connect it.
#     try:
#         con
#     except NameError:
#         # Connect to database
#         con = psycopg2.connect(database = SQL_DB, user = SQL_USER, password=SQL_PASSWORD, host=SQL_HOST)
#         cur = con.cursor()
#         cur.execute('SELECT version()')
#         version = cur.fetchone()[0]
#         print(f"DataBase Connected!\nVersion: {version}")
#         print('Initial connection to PostgreSQL DataBase')
#         print(con.closed)
#         return con, cur
#     else:
#         if con.closed !=0:
#         # Connect to database
#             con = psycopg2.connect(database = SQL_DB, user = SQL_USER, password=SQL_PASSWORD, host=SQL_HOST)
#             cur = con.cursor()
#             cur.execute('SELECT version()')
#             version = cur.fetchone()[0]
#             print(f"DataBase Connected!\nVersion: {version}")
#             print('Reconnected to PostgreSQL DataBase')
#             return con, cur
#         else:
#             print(f'PostgreSQL DataBase connection is normal.{con.closed}')
    