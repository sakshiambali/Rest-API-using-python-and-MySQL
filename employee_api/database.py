# database.py
# ──────────────────────────────────────────────────────────────
# This file is responsible for ONE thing: connecting Python to MySQL.
# Every other file that needs the database will import from here.
# ──────────────────────────────────────────────────────────────

import os                          # built-in module to read environment variables
import mysql.connector             # the package that lets Python talk to MySQL
from dotenv import load_dotenv     # reads key=value pairs from our .env file

# load_dotenv() finds the .env file and loads its values into os.environ
# After this line, os.getenv("DB_HOST") will return "localhost" (or whatever you set)
load_dotenv()


def get_connection():
    """
    Opens and returns a new MySQL connection.

    Why a function instead of a global variable?
    - A global connection can go stale (timeout, network drop).
    - A function gives you a fresh connection every time you ask for one.
    - It also makes error handling in one place easy.
    """
    try:
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST"),        # e.g. "localhost"
            port=int(os.getenv("DB_PORT")),   # MySQL default port is 3306
            user=os.getenv("DB_USER"),        # e.g. "root"
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")     # e.g. "employee_db"
        )
        return connection

    except mysql.connector.Error as error:
        # mysql.connector.Error covers all MySQL-related errors:
        # wrong password, database not found, MySQL server not running, etc.
        print(f"[DATABASE ERROR] Could not connect to MySQL: {error}")
        raise   # re-raise so the calling code knows something went wrong
