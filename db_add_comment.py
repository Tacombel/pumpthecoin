import sys
import sqlite3

hash = sys.argv[1]
comment = sys.argv[2]
print(f'Adding comment:{comment} to hash:{hash}.')

conn = sqlite3.connect("./contest/app.db")
cur = conn.cursor()
sql = "SELECT codigo, discord_user, nickname, comments, hash from users where hash = ? "
cursor = conn.execute(sql, (hash,))
row = cursor.fetchone()
sql = "REPLACE INTO users(codigo, discord_user, nickname, comments, hash) values (?,?,?,?,?)"
cur.execute(sql, (row[0], row[1], row[2], comment, hash))
conn.commit()
conn.close()
print(f'Now run python update_balance.py for the comments to show')
