import os

class Config(object):
    SECRET_KEY = os.getenv('SECRET_KEY', default='nuncasabras')
    discard_factor = os.getenv('SELL_DISCARD_FACTOR', default=5)
    orders_listed = os.getenv('ORDERS_LISTED', default=10)
    buy_order_limit = os.getenv('BUY_ORDER_LIMIT', default=80)
