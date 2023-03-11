import sqlite3


def connect_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn


def create_db():
    conn = sqlite3.connect("database.db")
    conn.execute("DROP TABLE IF EXISTS bots")
    # conn.execute('CREATE TABLE bots (id INTEGER PRIMARY KEY AUTOINCREMENT,container_id INTEGER)')
    conn.execute("CREATE TABLE bots (container_id INTEGER)")
    conn.close()


def bot_insert(id):
    conn = connect_db()
    conn.execute("INSERT INTO bots (container_id) VALUES (?)", (id,))
    conn.commit()
    conn.close()


def remove_bots():
    conn = connect_db()
    conn.execute("DELETE FROM bots")
    conn.commit()
    conn.close()


def show_bots():
    conn = connect_db()
    bots = conn.execute("SELECT container_id FROM bots").fetchall()
    conn.close()
    return bots

def count_bots():
    conn = connect_db()
    c = conn.cursor()
    c.execute('SELECT COUNT(*) FROM bots')
    result = c.fetchone()
    bot_count = result[0]
    conn.close()
    return bot_count
    
    
