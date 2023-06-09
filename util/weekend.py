import sqlite3
import json
from urllib.request import Request, urlopen
from urllib.error import URLError

def get_data(hash):
    initial_block = 240231
    final_block = 240663
    transactions = []
    url = 'https://explorer.scpri.me/navigator-api/hash/' + hash
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        response = urlopen(req)
        data = response.read()
        data = data.decode("utf-8")
        data = json.loads(data)
        if len(data) == 0:
            print(f'len(data)=0')
            return {'success':False, 'error':'There are no transactions on this address'}
        elif not data[1]["last100Transactions"]:
            print(f'not data[1]["last100Transactions"]')
            return {'success':False, 'error':'There are no transactions on this address'}
        else:
            totalScp = 0
            for e in data[1]["last100Transactions"]:
                if e["Height"] >=  initial_block and e["Height"] <= final_block:
                    totalScp += e["ScChange"] / 1E27
                    transactions.append(e)
            return {'success':True, 'totalScp':totalScp, 'transactions':transactions}
    except URLError as e:
        if hasattr(e, 'reason'):
            return {'success':False, 'error':'We failed to reach a server', 'reason':e.reason}
        elif hasattr(e, 'code'):
            return {'success':False, 'error':'The server couldn\'t fulfill the request', 'reason':e.code}
        
def get_balances():
    print(f'Weekend competition winners')
    conn = sqlite3.connect("../contest/app.db")
    cursor = conn.execute("SELECT nickname, hash from users")
    for e in cursor:
        data = get_data(e[1])
        if data["totalScp"] > 10000:
            print(f'>{e[0]} - {data["totalScp"]} scp')
            for d in data["transactions"]:
                print(d)
    conn.close()

if __name__ == '__main__':
    get_balances()
