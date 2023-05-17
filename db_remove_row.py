import sys
import sqlite3

hash = sys.argv[1]
print(f'Deleting {hash} from the database.')

conn = sqlite3.connect("./contest/app.db")
cur = conn.cursor()
sql = 'DELETE FROM users WHERE hash=?'
cur.execute(sql, (hash,))
sql = 'DELETE FROM balance WHERE hash=?'
cur.execute(sql, (hash,))
conn.commit()
conn.close()