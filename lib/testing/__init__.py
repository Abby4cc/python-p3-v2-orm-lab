from sqlite3 import connect

CONN = connect('database.db')
CURSOR = CONN.cursor()
