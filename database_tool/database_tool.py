'''
Created on Mar 22, 2014

@author: ioan
'''

import sqlite3
import os
import inspect


PWD = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
###     The database URL, something like:
###         "sqlite:///{database}.db"
###         "mysql+mysqlconnector://{user}:{password}@localhost/{database}"
DATABASE_URL = '../../ally/distribution/workspace/shared/application.db'
SQL_FILE = os.path.join(PWD, 'init_db.sql')


try:
    from settings_local import *
except Exception:
    pass


def initDB():
    print(SQL_FILE)
    print('--------------------init db---------------------------')
    sqlFile = open(SQL_FILE, 'r')
    sqlScript = sqlFile.read()
    sqlite3.complete_statement(sqlScript)
    connection = sqlite3.connect(DATABASE_URL)
    cursor = connection.cursor()
    try:
        cursor.executescript(sqlScript)
    except Exception as e:
        errorMessage = DATABASE_URL + ': ' + str(e)
        print(errorMessage)
        raise
    finally:
        cursor.close()
        connection.close()
        sqlFile.close()


if __name__ == '__main__':
    initDB()
