import sys
import sqlite3

column = sys.argv[1]
print(f'Adding column {column} to the database.')

conn = sqlite3.connect("./contest/app.db")
cur = conn.cursor()
sql = f'ALTER TABLE users ADD {column} TEXT'
cur.execute(sql)
conn.commit()
conn.close()