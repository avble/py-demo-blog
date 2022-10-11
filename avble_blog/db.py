import sqlite3
import os.path
from . import cfg

# Global variable for database
g_db = cfg.g_cfg['db_cfg']
DB_NAME = g_db['name']
DB_SCHEMA = g_db['schema']
DB_TEST_DATA = g_db['test_data']

# conn: represent a connection to datbase
# db: represent a database folder 
# prod: represent if it is prod environment  

def db_get() -> sqlite3.Connection:
    """
    support function:
    + return an instance of db connection
    """
    if 'conn' not in g_db:
        conn = sqlite3.connect(g_db['name'])
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
def post_read(id:int = 0)->list:
    db = db_get()
    cur = db.cursor()
    msg_query = f'select * from posts where id = {id}'
    print(f'DEBUG {msg_query}')
    data = cur.execute(msg_query)
    row = data.fetchone()
    return row


# post update
def post_update(id:int, title:str, content:str):
    db = db_get()
    cur = db.cursor()
    msg_query = f'update posts set title = "{title}", content = "{content}" where id = {id}'
    print(f'DEBUG {msg_query}')
    cur.execute(msg_query)

# post table manipulation
def posts_read(num_row:int = 10, limit_low = 0)->list:
    db = db_get()
    cur = db.cursor()
    msg_query = f'select * from posts LIMIT {limit_low}, 10'
    print(f'DEBUG {msg_query}')
    data = cur.execute(msg_query)
    rows = data.fetchmany(num_row)
    return rows


def posts_search(txt:str):
    db = db_get()
    cur = db.cursor()
    msg_query = "select * from posts where posts.content LIKE '%{txt}%'".format(txt=txt)
    print(f'DEBUG {msg_query}')
    data = cur.execute(msg_query)
    rows = data.fetchmany(100)
    return rows

g_db['prod'] = False
# db_init()
# print(posts_read())