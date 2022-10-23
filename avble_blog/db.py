import sqlite3
import psycopg2
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

def db_get():
    if 'conn' not in g_db:
        conn = psycopg2.connect(dbname='avbleblog', user='postgres', password='postgres', host='127.0.0.1', port=5433)
        conn.autocommit = True
        if conn != None:
            g_db['conn'] = conn
        else:
            print (f"can not connect to database")

    if 'conn' in g_db:
        return g_db['conn']
    else:
        return None

def db_init():

    conn = db_get()
    cur = conn.cursor()

    try:
        cur.execute("select * from version order by id desc")
        row = cur.fetchone()
        version = row[1] if row is not None else 0
    except:
        print ("the version table is not existed")
        version = -1

    if version == -1:
        db_execute_schema()

    # check if it is the prod or dev environment
    if 'prod' in g_db:
        if g_db['prod'] == False and (version == -1 or version == 0) :
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
    
    cur = db.cursor()
    cur.execute(sql_script)
    db.commit()
    
    print("Execute schema")

def db_add_test_data():
    """
    add data for testing purpose
    """
    sql_script = None
    with open (DB_TEST_DATA, encoding='utf-8') as f:
        sql_script = f.read()

    db = db_get()
    # db.executescript(sql_script)
    cur = db.cursor()
    cur.execute(sql_script)

def user_add(user, password):
    """
    Add a username and password to database
    """

# post table manipulation
def post_read(id:int = 0)->list:
    db = db_get()
    cur = db.cursor()
    msg_query = f'select * from posts where id = {id}'
    # print(f'DEBUG {msg_query}')
    cur.execute(msg_query)
    row = cur.fetchone()
    return row


# post update
def post_update(id:int, title:str, content:str):
    db = db_get()
    cur = db.cursor()
    msg_query = f"update posts set title = '{title}', content = '{content}' where id = {id}"
    # print(f'DEBUG {msg_query}')
    cur.execute(msg_query)
    db.commit()

# post delete
def posts_delete(id:int):
    db = db_get()
    cur = db.cursor()
    msg_query = f'delete from posts where id = {id}'
    cur.execute(msg_query)
    db.commit()

# post table manipulation
def posts_read(num_row:int = 10, limit_low = 0)->list:
    db = db_get()
    cur = db.cursor()
    msg_query = f'select * from posts ORDER BY ID ASC LIMIT {num_row} offset {limit_low}'
    # print(f'DEBUG {msg_query}')
    cur.execute(msg_query)
    rows = cur.fetchmany(num_row)
    return rows

def posts_search(txt:str):
    db = db_get()
    cur = db.cursor()
    msg_query = "select * from posts where posts.content LIKE '%{txt}%'".format(txt=txt)
    # print(f'DEBUG {msg_query}')
    cur.execute(msg_query)
    rows = cur.fetchmany(100)
    return rows

g_db['prod'] = False
# db_init()
# print(posts_read())