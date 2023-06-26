from urllib.request import Request, urlopen
from urllib.error import URLError
import json
import sqlite3
import logging
import os

LOGLEVEL = os.environ.get('LOGLEVEL', 'DEBUG').upper()
logger = logging.getLogger(__name__)
c_handler = logging.StreamHandler()
c_handler.setLevel(LOGLEVEL)
c_format = logging.Formatter('%(asctime)s %(levelname)s %(name)s : %(message)s')
c_handler.setFormatter(c_format)
logger.addHandler(c_handler)
logger.setLevel(LOGLEVEL)

logger.info(f'LOGLEVEL: {LOGLEVEL}')

start_height = 238650
end_height = 244701
def get_data(hash):
    url = 'https://explorer.scpri.me/navigator-api/hash/' + hash
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        response = urlopen(req)
        data = response.read()
        data = data.decode("utf-8")
        data = json.loads(data)
        if len(data) == 0:
            logger.info(f'len(data)=0')
            return {'success':False, 'error':'There are no transactions on this address'}
        elif not data[1]["last100Transactions"]:
            logger.info(f'not data[1]["last100Transactions"]')
            return {'success':False, 'error':'There are no transactions on this address'}
        else:
            totalScp = 0
            for e in data[1]["last100Transactions"]:
                if e["Height"] > start_height and e["Height"] >= end_height:
                    totalScp += e["ScChange"]
            return {'success':True, 'totalScp':totalScp}
    except URLError as e:
        if hasattr(e, 'reason'):
            return {'success':False, 'error':'We failed to reach a server', 'reason':e.reason}
        elif hasattr(e, 'code'):
            return {'success':False, 'error':'The server couldn\'t fulfill the request', 'reason':e.code}

def add_entry(discord_user, nickname, hash):
    check_if_exists = get_data(hash)
    if not check_if_exists["success"]:
        return {'success': False, 'error': 'You can´t add a hash until there is at least one transaction'}
    conn = sqlite3.connect("./contest/app.db")
    try:
        conn.execute("INSERT INTO users(discord_user, nickname, hash) values (?,?,?)", (discord_user, nickname, hash))
        conn.commit()
        data = get_data(hash)
        if data["success"]:
            conn.execute("REPLACE INTO balance(nickname, hash, amount) values (?,?,?)", (nickname, hash, '{:.3f}'.format(data["totalScp"] / 1e27)))
            conn.commit()
        conn.close()
        logger.info(f'{discord_user} added to the database')
        return {'success':True, 'message':'Entry added to the database'}
    except sqlite3.IntegrityError:
        return {'success': False, 'error': 'This hash already exists in the database'}

def get_balances():
    conn = sqlite3.connect('./contest/app.db')
    sql = 'SELECT users.nickname, users.hash, amount, comments from users INNER JOIN balance ON users.hash = balance.hash  ORDER BY amount DESC'
    cursor = conn.execute(sql)
    lines = []
    total_participating = 0
    for e in cursor:
        lines.append(e)
        total_participating += e[2]
    total_participating = int(total_participating)
    return {"lines":lines, "total_participating":total_participating}
