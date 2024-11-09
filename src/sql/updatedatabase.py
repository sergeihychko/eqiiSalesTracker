import sqlite3

from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker

from src.data import salesitem


def update(rows:list[salesitem]):
    """
    Update the database of all rows in the list of dataclass salesitem
    :param rows:
    :return:
    """
    # Create an engine to connect to your database
    engine = create_engine('sqlite:///eqiisales.db')

    # Access the metadata associated with the engine
    metadata = MetaData()
    metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    for sitem in rows:
        session.add(sitem)

    session.commit()


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