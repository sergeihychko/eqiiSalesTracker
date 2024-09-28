import sqlite3

from data import salesitem


def update(rows:list[salesitem]):

    conn = sqlite3.connect('eqiisales.db')
    c = conn.cursor()
    for sitem in rows:
        sqlstatement = """CREATE TABLE IF NOT EXISTS rawsales (
                id TEXT PRIMARY KEY, 
                server TEXT,
                seller TEXT,
                salesdate TEXT,
                description TEXT,
                price TEXT,
                absoluteprice REAL
        );"""
        c.execute(sqlstatement)
        conn.commit()
        c.execute("INSERT INTO rawsales (id, server, seller, salesdate, description, price) VALUES (?, ?, ?, ?, ?, ?)",
                  (sitem.id, sitem.server, sitem.seller, sitem.salesdate, sitem.description, sitem.price))
        conn.commit()

    conn.close()

def dump():
    conn = sqlite3.connect('../eqiisales.db')
    c = conn.cursor()
    c.execute("SELECT Count() from rawsales")

    conn.close()

class UpdateDatabase:
    pass