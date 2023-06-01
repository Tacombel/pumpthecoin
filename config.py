import os

class Config(object):
    SECRET_KEY = os.getenv('SECRET_KEY', default='nuncasabras')
    discard_factor = int(os.getenv('SELL_DISCARD_FACTOR', default=5))
    orders_listed = int(os.getenv('ORDERS_LISTED', default=10))
    buy_order_limit = int(os.getenv('BUY_ORDER_LIMIT', default=80))
    # telegram
    # Your Telegram Token. Search @BotFather and create BOT
    telegram_token =  os.getenv('TELEGRAM_TOKEN')
    # Your ID User. Search @userinfobot. There will be several. Keep testing until one answer with something like Id:56869524
    user_id = os.getenv('USER_ID')