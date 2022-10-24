import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    discard_factor = os.environ.get('SELL_DISCARD_FACTOR') or 5
    orders_listed = os.environ.get('ORDERS_LISTED') or 10
    buy_order_limit = os.environ.get('BUY_ORDER_LIMIT') or 80
