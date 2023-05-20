from subprocess import Popen
from apscheduler.schedulers.background import BackgroundScheduler
import sqlite3

bind = "0.0.0.0:5200"
workers = 3
timeout = 120
access_log_format = '%(h)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" "%({X-Forwarded-For}i)s" "%({X-Forwarded-Port}i)s" "%({X-Forwarded-Proto}i)s"  "%({X-Amzn-Trace-Id}i)s"'
max_requests = 16384
limit_request_line = 8190
keepalive = 60

def update():
    print("Starting update process...")
    po = Popen("python update_balance.py", shell=True)
    print("Update started as PID %d", po.pid)
    rc = po.wait()
    print("Update process finished with status code %d", rc)


sched = None

def on_starting(server):
    print(f'Initializing the database...')
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
        comments text,
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
    
    print("Initial database load...")
    po = Popen("python3 update_balance.py", shell=True)
    print(f'Update started as PID {po.pid}')
    rc = po.wait()
    print(f'Update process finished with status code {rc}')

    print("Starting scheduler...")
    global sched
    sched = BackgroundScheduler(timezone="UTC", daemon=True)
    #sched.add_job(update, id="update", coalesce=True, max_instances=1, trigger='interval', minutes=60)
    sched.add_job(update, id="update", max_instances=1, trigger='interval', minutes=60)
    sched.start()
