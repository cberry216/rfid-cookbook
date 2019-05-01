import sqlite3
import sys


def build_database(connection, cursor):
    sql = "CREATE TABLE recipe (id INTEGER PRIMARY KEY AUTOINCREMENT, name VARCHAR(80) NOT NULL, ingredients TEXT NOT NULL, instructions TEXT NOT NULL);"
    cursor.execute(sql)
    connection.commit()
