from flask import Flask
from dotenv import load_dotenv
import os
import logging

load_dotenv()
LOGLEVEL = os.environ.get('LOGLEVEL', 'INFO').upper()
#logging.basicConfig(filename = 'filename.log', level=logging.<log_level>, format = '<message_structure>')
logging.basicConfig(level=LOGLEVEL, format = f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
logging.info(f'LOGLEVEL: {LOGLEVEL}')
logging.debug(f'Using secret key: {os.getenv("SECRET_KEY")}')

app = Flask(__name__)
from app import routes
