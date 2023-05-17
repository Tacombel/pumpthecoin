import sys
import sqlite3

hash = sys.argv[1]
print(f'Deleting {hash} from the database.')

conn = sqlite3.connect("./contest/app.db")
sql = 'DELETE FROM USERS WHERE hash=?'
cur = conn.cursor()
cur.execute(sql, (hash,))
conn.commit()
conn.close()