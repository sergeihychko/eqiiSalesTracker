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

def get_seller_list():
    """
    queries the rawsales table in the database for unique seller entries
    :return: a complete list of sellers or null
    """
    results = []
    conn = sqlite3.connect('eqiisales.db')
    c = conn.cursor()
    try:
        c.execute("SELECT DISTINCT seller FROM rawsales;")
        results = c.fetchall()
    except:
        print("Error: querying rawsales table")
    conn.commit()
    conn.close()
    return results

def retrieve_seller_data(seller):
    """
    return all rows in the rawsales table where seller = :param
    :param seller: seller in rawsales table
    :return: all rows connected to seller in rawsales table
    """
    results = []
    conn = sqlite3.connect('eqiisales.db')
    c = conn.cursor()
    query = "SELECT * FROM rawsales where seller = ?;"
    print("query is : " + query)
    try:
        c.execute(query, (seller,))
        results = c.fetchall()
    except Exception as err:
        print("Error: querying rawsales table for seller: " + str(err))
    conn.commit()
    conn.close()
    return results

class UpdateDatabase:
    pass