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

root_url = 'https://tradeogre.com/api/v1'
def get_order_book():
    root_url = 'https://tradeogre.com/api/v1'
    url = root_url + '/orders/BTC-SCP'
    orders = requests.get(url)
    orders = json.loads(orders.text)
    buy_orders = orders["buy"]
    buy_orders_list = []
    for k in buy_orders:
        buy_orders_list.append([float(k), float(buy_orders[k])])
    sell_orders = orders["sell"]
    sell_orders_list = []
    for k in sell_orders:
        sell_orders_list.append([float(k), float(sell_orders[k])])
    return buy_orders_list, sell_orders_list

def list_orders():
    price = btc_price()
    buy_orders_list, sell_orders_list = get_order_book()
    buy_orders_list = buy_orders_list[-5:]
    sell_orders_list = sell_orders_list[0:5]
    for e in reversed(sell_orders_list):
        print(f'TO: {float(e[1]):.2f} SCP {e[0]} BTC - ${float(e[0]) * price:.4f} Value: ${float(e[1]) * float(e[0]) * price:.2f}')
    print('-----------------------')
    for e in reversed(buy_orders_list):
        print(f'TO: {float(e[1]):.2f} SCP {e[0]} BTC - ${float(e[0]) * price:.4f} Value: ${float(e[1]) * float(e[0]) * price:.2f}')

if __name__ == "__main__":
    list_orders()