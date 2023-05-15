from urllib.request import Request, urlopen
from urllib.error import URLError
import json
import sqlite3
from time import time

try:
    with open('./contest/app.db', 'x') as f:
        pass
except FileExistsError:
    pass
conn = sqlite3.connect("./contest/app.db")
try:
    conn.execute("""create table users (
    codigo integer primary key autoincrement,
    discord_user text,
    nickname text,
    hash text,
    UNIQUE(hash)
    )""")
    print(f'Tabla usuarios creada')
except sqlite3.OperationalError:
    print(f'La tabla users ya existe')
try:
    conn.execute("""create table balance (
    hash TEXT primary key,
    nickname TEXT,
    amount REAL
    )""")
    print(f'Tabla balance creada')
except sqlite3.OperationalError:
    print(f'La tabla balance ya existe')
try:
    conn.execute("""create table variables (
    name TEXT primary key,
    value REAL
    )""")
    print(f'Tabla variables creada')
except sqlite3.OperationalError:
    print(f'La tabla variables ya existe')
conn.close()

start_height = 0

def get_data(hash):
    url = 'https://explorer.scpri.me/navigator-api/hash/' + hash
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        response = urlopen(req)
        data = response.read()
        data = data.decode("utf-8")
        data = json.loads(data)
        if len(data) == 0:
            return {'success':False, 'error':'There are no transactions on this address'}
        else:
            totalScp = 0
            for e in data[1]["last100Transactions"]:
                if e["Height"] > start_height:
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
        conn.close()
        return {'success':True, 'message':'Entry added to the database'}
    except sqlite3.IntegrityError:
        return {'success': False, 'error': 'This hash already exists in the database'}
