from subprocess import Popen
from apscheduler.schedulers.background import BackgroundScheduler
import sqlite3
import logging
import os

bind = "0.0.0.0:5200"
workers = 3
timeout = 120
access_log_format = '%(h)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" "%({X-Forwarded-For}i)s" "%({X-Forwarded-Port}i)s" "%({X-Forwarded-Proto}i)s"  "%({X-Amzn-Trace-Id}i)s"'
max_requests = 16384
limit_request_line = 8190
keepalive = 60

LOGLEVEL = os.environ.get('LOGLEVEL', 'DEBUG').upper()
#logging.basicConfig(filename = 'filename.log', level=logging.<log_level>, format = '<message_structure>')
logging.basicConfig(level=LOGLEVEL, format = f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
logging.info(f'LOGLEVEL: {LOGLEVEL}')

def update():
    logging.info("Starting update process...")
    po = Popen("python update_balance.py", shell=True)
    logging.info("Update started as PID %d", po.pid)
    rc = po.wait()
    logging.info("Update process finished with status code %d", rc)


sched = None

def on_starting(server):
    logging.info(f'Initializing the database...')
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
        logging.info(f'Tabla usuarios creada')
    except sqlite3.OperationalError:
        logging.info(f'La tabla users ya existe')
    try:
        conn.execute("""create table balance (
        hash TEXT primary key,
        nickname TEXT,
        amount REAL
        )""")
        logging.info(f'Tabla balance creada')
    except sqlite3.OperationalError:
        logging.info(f'La tabla balance ya existe')
    try:
        conn.execute("""create table variables (
        name TEXT primary key,
        value REAL
        )""")
        logging.info(f'Tabla variables creada')
    except sqlite3.OperationalError:
        logging.info(f'La tabla variables ya existe')
    conn.close()
    
    logging.info("Initial database load...")
    po = Popen("python3 update_balance.py", shell=True)
    logging.info(f'Update started as PID {po.pid}')
    rc = po.wait()
    logging.info(f'Update process finished with status code {rc}')

    logging.info("Starting scheduler...")
    global sched
    sched = BackgroundScheduler(timezone="UTC", daemon=True)
    #sched.add_job(update, id="update", coalesce=True, max_instances=1, trigger='interval', minutes=60)
    sched.add_job(update, id="update", max_instances=1, trigger='interval', minutes=60)
    sched.start()
