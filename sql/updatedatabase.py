import sqlite3

from data import salesitem


def update(rows:list[salesitem]):

    conn = sqlite3.connect('eqiisales.db')
    c = conn.cursor()
    for sitem in rows:
        c.execute("INSERT INTO rawsales (id, server, seller, salesdate, description, price) VALUES (?, ?, ?, ?, ?, ?)",
                  (sitem.id, sitem.server, sitem.seller, sitem.salesdate, sitem.description, sitem.price))
        conn.commit()

    conn.close()


class UpdateDatabase:
    pass