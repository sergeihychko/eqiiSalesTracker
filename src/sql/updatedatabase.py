import sqlite3

from src.data import salesitem


def update(rows:list[salesitem]):

    conn = sqlite3.connect('eqiisales.db')
    c = conn.cursor()
    for sitem in rows:
        sqlstatement = """CREATE TABLE IF NOT EXISTS rawsales (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                server TEXT,
                seller TEXT,
                salesdate TEXT,
                description TEXT,
                price TEXT,
                absoluteprice REAL
        );"""
        c.execute(sqlstatement)
        conn.commit()
        c.execute("INSERT INTO rawsales (server, seller, salesdate, description, price) VALUES (?, ?, ?, ?, ?)",
                  (sitem.server, sitem.seller, sitem.salesdate, sitem.description, sitem.price))
        conn.commit()

    conn.close()

def dump():
    conn = sqlite3.connect('eqiisales.db')
    c = conn.cursor()
    try:
        c.execute("DROP TABLE IF EXISTS rawsales")
        c.execute("DROP TABLE rawsales")
    except:
        print("Error: dropping table")

    conn.commit()
    conn.close()

class UpdateDatabase:
    pass