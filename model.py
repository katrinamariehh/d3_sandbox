import sqlite3

ADMIN_USER="hackbright"
ADMIN_PASSWORD=5980025637247534551

DB = None
CONN = None

def authenticate(username, password):
    query = """SELECT username, password FROM users WHERE username = ?"""
    DB.execute(query, (username,))
    row = DB.fetchone()

    if hash(password) == row[1]:
        return username
    else:
        return None

def connect_to_db():
    global DB, CONN
    CONN = sqlite3.connect("thewall.db")
    DB = CONN.cursor()