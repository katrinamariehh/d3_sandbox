import sqlite3

ADMIN_USER="hackbright"
ADMIN_PASSWORD=5980025637247534551

DB = None
CONN = None

def connect_to_db():
    global DB, CONN
    CONN = sqlite3.connect("thewall.db")
    DB = CONN.cursor()

def authenticate(username, password):
    query = """SELECT id, username, password FROM users WHERE username = ?"""
    DB.execute(query, (username,))
    row = DB.fetchone()

    if hash(password) == int(row[2]):
        return row[0]
    else:
        return None

def get_user_by_name(username):
    query = """SELECT id FROM users WHERE username = ?"""
    DB.execute(query, (username,))
    row = DB.fetchone()
    if row:
        return row[0]
    else:
        return None

def get_wall_posts_for_user(user_id):
    query = """SELECT users.username, created_at, content FROM wall_posts JOIN users ON (author_id = users.id) WHERE owner_id = ?"""
    DB.execute(query, (user_id,))
    rows = DB.fetchall()

    return rows

def add_wall_post(current_user, wall_owner, wall_content):
    query = """INSERT INTO wall_posts (owner_id, author_id, created_at, content) VALUES (?, ?, CURRENT_TIMESTAMP, ?)"""
    DB.execute(query, (wall_owner, current_user, wall_content))
    CONN.commit()

def add_new_user(username, password):
    query = """INSERT INTO users (username, password) VALUES (?, ?)"""
    DB.execute(query, (username, hash(password)))
    CONN.commit()


def main():
    connect_to_db()

if __name__ == "__main__":
    main()