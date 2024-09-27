import sqlite3


def create_tables(database):
    db_name = "'" + database + "'"
    sql_statements = [
        """DROP TABLE rawsales;
        """,
        """CREATE TABLE IF NOT EXISTS rawsales (
                id TEXT PRIMARY KEY, 
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
                print("statement :" + statement + " was executed")

            conn.commit()
    except sqlite3.Error as e:
        print(e)
    print("database :" + db_name + " was created")

if __name__ == '__main__':
    create_tables()