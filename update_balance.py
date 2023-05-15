import sqlite3
from contest import get_data
from time import time

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

if __name__ == "__main__":
    get_balances()
