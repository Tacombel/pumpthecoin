import sqlite3
import csv
from contest import get_data
import os
import logging

LOGLEVEL = os.environ.get('LOGLEVEL', 'DEBUG').upper()
logger = logging.getLogger(__name__)
c_handler = logging.StreamHandler()
c_handler.setLevel(LOGLEVEL)
c_format = logging.Formatter('%(asctime)s %(levelname)s %(name)s : %(message)s')
c_handler.setFormatter(c_format)
logger.addHandler(c_handler)
logger.setLevel(LOGLEVEL)

logger.info(f'LOGLEVEL: {LOGLEVEL}')

def get_balances():
    # Loading ban list
    try:
        with open('./contest/ban_list.txt', mode='r') as file:
            banned = file.readlines()
        logger.debug(f'Updating balances')
        conn = sqlite3.connect("./contest/app.db")
        cursor = conn.execute("SELECT nickname, hash from users")
        for e in cursor:
            if e[1] in banned:
                logger.info(f'Setting banned contestant {e[0]} to 0 scp')
                conn.execute("REPLACE INTO balance(nickname, hash, amount) values (?,?,?)", (e[0], e[1], 0))
                conn.commit()
            else:
                data = get_data(e[1])
                if data["success"]:
                    conn.execute("REPLACE INTO balance(nickname, hash, amount) values (?,?,?)", (e[0], e[1], '{:.3f}'.format(data["totalScp"] / 1e27)))
                    conn.commit()
        conn.close()
    except FileNotFoundError:
        logger.info('There is no ban_list.txt')
    


def write_csv():
    conn = sqlite3.connect("./contest/app.db")
    cur = conn.cursor()
    sql = 'SELECT discord_user, users.nickname, users.hash, amount, comments from users INNER JOIN balance ON users.hash = balance.hash;'
    cur.execute(sql)
    result = cur.fetchall()
    
    with open('./contest/db_backup.csv', mode='w') as csv_file:
        fieldnames = ['discord_user', 'nickname', 'hash', 'amount']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for row in result:
            writer.writerow({'discord_user':row[0], 'nickname':row[1], 'hash':row[2], 'amount':row[3]})

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    get_balances()
    write_csv()
