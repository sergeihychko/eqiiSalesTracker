import sqlite3


def create_tables():
    sql_statements = [
        """CREATE TABLE IF NOT EXISTS rawsales (
                id INTEGER PRIMARY KEY, 
                server TEXT,
                seller TEXT,
                salesdate TEXT,
                description TEXT,
                price TEXT,
                absoluteprice REAL
        );"""]

    # create a database connection
    try:
        #with sqlite3.connect('eqiisales.db') as conn:
        with sqlite3.connect(':memory:') as conn:
            cursor = conn.cursor()
            for statement in sql_statements:
                cursor.execute(statement)

            conn.commit()
    except sqlite3.Error as e:
        print(e)


if __name__ == '__main__':
    create_tables()