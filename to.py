import requests
import json
from time import time

cache_timer = 60
price_btc = [0, 0]
def btc_price():
    global price_btc
    if time() > price_btc[1] + cache_timer or price_btc[1] == 0:
        btc = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd')
        btc = btc.json()
        btc = float(btc['bitcoin']['usd'])
        price_btc = [btc, time()]
    else:
        btc = price_btc[0]
    return btc

# https://tradeogre.com/api/v1/orders/BTC-SCP
def get_order_book():
    price = btc_price()
    root_url = 'https://tradeogre.com/api/v1'
    url = root_url + '/orders/BTC-SCP'
    orders = requests.get(url)
    orders = json.loads(orders.text)
    buy_orders = orders["buy"]
    buy_orders_list = []
    for k in buy_orders:
        buy_orders_list.append(['TO', 'BTC', float(buy_orders[k]), float(k), float(k) * price, float(k) * float(buy_orders[k]) * price])
    sell_orders = orders["sell"]
    sell_orders_list = []
    for k in sell_orders:
        sell_orders_list.append(['TO', 'BTC', float(sell_orders[k]), float(k), float(k) * price, float(k) * float(sell_orders[k]) * price])
    return buy_orders_list, sell_orders_list

def list_orders():
    def output(e):
        print(f'Market: {e[0]} - Book: {e[1]} - Amount: {e[2]} - Price: {e[3]} - Price($): {e[4]} - Value: {e[5]}')
    buy_orders_list, sell_orders_list = get_order_book()
    buy_orders_list = buy_orders_list[-10:]
    sell_orders_list = sell_orders_list[0:10]
    for e in reversed(sell_orders_list):
        output(e)
    print('-----------------------')
    for e in reversed(buy_orders_list):
        output(e)

if __name__ == "__main__":
    list_orders()