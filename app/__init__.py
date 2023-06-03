from flask import Flask
from dotenv import load_dotenv
import os
import logging

load_dotenv()
LOGLEVEL = os.environ.get('LOGLEVEL', 'DEBUG').upper()
logger = logging.getLogger(__name__)
c_handler = logging.StreamHandler()
c_handler.setLevel(LOGLEVEL)
c_format = logging.Formatter('%(asctime)s %(levelname)s %(name)s : %(message)s')
c_handler.setFormatter(c_format)
logger.addHandler(c_handler)
logger.setLevel(LOGLEVEL)

logger.info(f'LOGLEVEL: {LOGLEVEL}')
logger.debug(f'Using secret key: {os.getenv("SECRET_KEY")}')

app = Flask(__name__)
from app import routes
