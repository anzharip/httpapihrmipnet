import pymysql
import config

def open_connection():
    return pymysql.connect(host=config.DBHOST, user=config.DBUSER, password=config.DBPASS, db=config.DBNAME, port=config.DBPORT, connect_timeout=5)

def sql_cursor(connection, statement):
    cursor = connection.cursor()
    sql = statement
    cursor.execute(sql)
    return cursor

def close_connection(cursor, connection):
    cursor.close()
    connection.close()