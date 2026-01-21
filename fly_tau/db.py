import mysql.connector
from contextlib import contextmanager
'''MYSQL CONNECTION'''
@contextmanager
def db_cur(dictionary=False):
    #Context manager that yields a database cursor and ensures the connection is automatically closed after use.
    mydb= None
    cursor = None
    try:
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="fly_tau_db",
            autocommit=True)
        cursor = mydb.cursor(dictionary=dictionary)
        yield cursor
    except mysql.connector.Error as err:
        raise err
    finally:
        if cursor:
            cursor.close()
        if mydb:
            mydb.close()



