import os
import sqlite3

import sqlalchemy
from sqlalchemy import create_engine, MetaData


def create_tables(database):
    # the relative file path
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, "eqiisales.db")
    print("sql alchemy version : " + sqlalchemy.__version__)

    sql_statements = [
        """CREATE TABLE IF NOT EXISTS rawsales (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                server TEXT,
                seller TEXT,
                salesdate TEXT,
                description TEXT,
                price TEXT,
                absoluteprice REAL
        );"""]

    # create a database connection
    try:
        with sqlite3.connect('eqiisales.db') as conn:
            cursor = conn.cursor()
            for statement in sql_statements:
                cursor.execute(statement)

            conn.commit()
    except sqlite3.Error as e:
        print(e)

def dump():
    """
    function that will drop the existing database table(s)
    :return:
    """
    print("sql alchemy version : " + sqlalchemy.__version__)

    # Create an engine to connect to your database
    engine = create_engine('sqlite:///eqiisales.db')

    # Access the metadata associated with the engine
    metadata = MetaData()

    # Reflect the database schema into the metadata
    metadata.reflect(bind=engine)

    # Get the table object you want to drop
    table_name = 'rawsales'
    table = metadata.tables.get(table_name)

    if table is not None:
        # Drop the table
        table.drop(engine)
        print(f"Table '{table_name}' dropped successfully.")
    else:
        print(f"Table '{table_name}' not found.")


if __name__ == '__main__':
    create_tables()