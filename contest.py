from urllib.request import Request, urlopen
from urllib.error import URLError
import json
from time import time

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

def add_entry(nickname, hash):
    entries = []
    try:
        with open('./contest/entries.txt', 'r') as f:
            for line in f:
                line = json.loads(line)
                entries.append(line)
            for entry in entries:
                if hash in entry:
                    return {'success': False, 'error': 'hash already in database'}
    except FileNotFoundError:
        pass
    check_if_exists = get_data(hash)
    if not check_if_exists["success"]:
        return {'success': False, 'error': 'You can´t add a hash until there is at least one transaction'}
    entries.append([nickname, hash, time()])
    with open('./contest/entries.txt', 'w+') as f:
        for e in entries:
            f.write(json.dumps(e))
            f.write('\n')
    return {'success':True, 'message':'Entry added to the database'}

def get_balances():
    entries = []
    try:
        with open('./contest/entries.txt', 'r') as f:
            for line in f:
                line = json.loads(line)
                entries.append(line)
    except FileNotFoundError:
        return {'success': False, 'error': 'There are no entries on the database', 'lines':[['', '', '']]}
    results_lines = []
    for e in entries:
        data = get_data(e[1])
        if data["success"]:
            results_lines.append([e[0], e[1], '{:.3f}'.format(data["totalScp"] / 1e27)])
    results_lines.sort(key=lambda a: a[2], reverse=True)
    return {'success': True, 'lines': results_lines}

def main():
     #test_add_entry()
     for e in get_balances()["lines"]:
         print(e)

if __name__ == "__main__":
    main()
