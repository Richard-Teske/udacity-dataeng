import psycopg2
from sql_queries import create_table_queries, drop_table_queries


def connection(host="127.0.0.1", dbname="sparkifydb", user="student", password="student"):
    """
    - Creates postgres connection
    - Returns connection
    """
    conn = psycopg2.connect(f"host={host} dbname={dbname} user={user} password={password}")
    conn.set_session(autocommit=True)
    return conn

def create_database():
    """
    - Creates and connects to the sparkifydb
    - Returns the connection and cursor to sparkifydb
    """
    
    # connect to default database
    conn = connection()
    cur = conn.cursor()
    
    # create sparkify database with UTF8 encoding
    cur.execute("DROP DATABASE IF EXISTS sparkifydb")
    cur.execute("CREATE DATABASE sparkifydb WITH ENCODING 'utf8' TEMPLATE template0")

    # close connection to default database
    conn.close()

def drop_tables():
    """
    Drops each table using the queries in `drop_table_queries` list.
    """
    conn = connection()
    cur = conn.cursor()

    for query in drop_table_queries:
        cur.execute(query)
        conn.commit()
    conn.close()

def create_tables():
    """
    Creates each table using the queries in `create_table_queries` list. 
    """
    conn = connection()
    cur = conn.cursor()

    for query in create_table_queries:
        cur.execute(query)
        conn.commit()
    
    conn.close()

def main():
    """
    - Drops (if exists) and Creates the sparkify database. 

    - Drops all the tables.  
    
    - Creates all tables needed. 
    
    - Finally, closes the connection. 
    """
    #create_database()
    drop_tables()
    create_tables()

if __name__ == "__main__":
    main()