from genericpath import isfile
import sqlite3
import os.path

DB_NAME = "blog.db"
DB_SCHEMA = "schema.sql"
DB_TEST_DATA = "test_data.sql"

# Global variable for database
g_db = {}
# conn: represent a connection to datbase
# db: represent a database folder 
# prod: represent if it is prod environment  

def db_get() -> sqlite3.Connection:
    """
    support function:
    + return an instance of db connection
    """
    if 'conn' not in g_db:
        conn = sqlite3.connect(DB_NAME)
        if conn != None:
            g_db['conn'] = conn
        else:
            print (f"can not open database:{DB_NAME}")

    if 'conn' in g_db:
        return g_db['conn']
    else:
        return None

def db_init():
    """
    Create a database if it does not exists
    """
    # If the db has not there, create the database
    if not os.path.isfile(DB_NAME):
        print ("Create database ")
        db_execute_schema()

    # check if it is the prod or dev environment
    if 'prod' in g_db:
        if g_db['prod'] == False:
            db_add_test_data()
   
def db_close():
    """
    close the connection
    """
    if 'conn' in g_db:
        conn = db_get()
        conn.close()
        del g_db['conn']

def db_execute_schema():
    """
    Execute the database schema
    """
    with open(DB_SCHEMA, encoding='utf-8') as f:
        sql_script = f.read()
        # print (sql_script)

    db = db_get()
    db.executescript(sql_script)
    db.commit()
    
    print("Execute schema")
    pass

def db_add_test_data():
    """
    add data for testing purpose
    """
    sql_script = None
    with open (DB_TEST_DATA, encoding='utf-8') as f:
        sql_script = f.read()

    db = db_get()
    db.executescript(sql_script)

def user_add(user, password):
    """
    Add a username and password to database
    """


# post table manipulation
def post_read():
    db = db_get()
    cur = db.cursor()
    data = cur.execute('select * from posts')
    rows = data.fetchmany(10)
    return rows

g_db['prod'] = False
# db_init()
# print(post_read())