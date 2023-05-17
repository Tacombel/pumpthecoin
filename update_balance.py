import sqlite3
import csv
from contest import get_data

def get_balances():
    print(f'Updating balances')
    conn = sqlite3.connect("./contest/app.db")
    cursor = conn.execute("SELECT nickname, hash from users")
    for e in cursor:
        data = get_data(e[1])
        if data["success"]:
            conn.execute("REPLACE INTO balance(nickname, hash, amount) values (?,?,?)", (e[0], e[1], '{:.3f}'.format(data["totalScp"] / 1e27)))
            conn.commit()
    conn.close()

def write_csv():
    conn = sqlite3.connect("./contest/app.db")
    cur = conn.cursor()
    sql = 'SELECT discord_user, users.nickname, users.hash, amount from users INNER JOIN balance ON users.hash = balance.hash;'
    cur.execute(sql)
    result = cur.fetchall()
    
    with open('./contest/db_backup.csv', mode='w') as csv_file:
        fieldnames = ['discord_user', 'nickname', 'hash', 'amount']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for row in result:
            writer.writerow({'discord_user':row[0], 'nickname':row[1], 'hash':row[2], 'amount':row[3]})

if __name__ == "__main__":
    get_balances()
    write_csv()
