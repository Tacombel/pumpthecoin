import requests
import sys
from config import Config
from operator import itemgetter
from time import time
import json

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

price_spc = [0, 0]
def spc_price():
    global price_spc
    if time() > price_spc[1] + cache_timer or price_spc[1] == 0:
        spc = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=siaprime-coin&vs_currencies=btc%2Cusd')
        spc = spc.json()
        spc = spc['siaprime-coin']['usd']
        price_spc = [spc, time()]
    else:
        spc = price_spc[0]
    return spc

price_usdt = [0, 0]
def usdt_price():
    global price_usdt
    if time() > price_usdt[1] + cache_timer or price_usdt[1] == 0:
        usdt = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=tether&vs_currencies=usd')
        usdt = usdt.json()
        usdt = usdt['tether']['usd']
        price_usdt = [usdt, time()]
    else:
        usdt = price_usdt[0]
    return usdt

price_eth = [0, 0]
def eth_price():
    global price_eth
    if time() > price_eth[1] + cache_timer or price_eth[1] == 0:
        eth = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd')
        eth = eth.json()
        eth = eth['ethereum']['usd']
        price_eth = [eth, time()]
    else:
        eth = price_eth[0]
    return eth

price_ltc = [0, 0]
def ltc_price():
    global price_ltc
    if time() > price_ltc[1] + cache_timer or price_ltc[1] == 0:
        ltc = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=litecoin&vs_currencies=usd')
        ltc = ltc.json()
        ltc = ltc['litecoin']['usd']
        price_ltc = [ltc, time()]
    else:
        ltc = price_ltc[0]
    return ltc

def data(target_price):
    target = target_price / btc_price()
    data = requests.get('https://www.southxchange.com/api/book/SCP/BTC')
    data = data.json()['SellOrders']
    neccesary_amount = 0
    units = 0
    for e in data:
        if float(e['Price']) < target:
            neccesary_amount += float(e['Amount']) * float(e['Price'])
            units += float(e['Amount'])
    return btc_price(), target, neccesary_amount, units

# 'https://www.southxchange.com/api/book/SCP/BTC', 'https://www.southxchange.com/api/book/SCP/USDT', 'https://www.southxchange.com/api/book/SCP/ETH', 'https://www.southxchange.com/api/book/SCP/LTC']
def get_sx_orders(book_url):
    type = book_url.split('/')[6]
    if type == 'BTC':
        price = btc_price()
    elif type == 'USDT':
        price = usdt_price()
    elif type == 'LTC':
        price = ltc_price()
    elif type == 'ETH':
        price = eth_price()
    data = requests.get(book_url)
    buyorders = data.json()['BuyOrders']
    buyorders_list = []
    for order in buyorders:
        buyorders_list.append(['SX', type, order['Amount'], order['Price'], order['Price'] * price, order['Amount'] * order['Price'] * price])
    sellorders = data.json()['SellOrders']
    sellorders_list = []
    for order in sellorders:
        sellorders_list.append(['SX', type, order['Amount'], order['Price'], order['Price'] * price, order['Amount'] * order['Price'] * price])
    return [buyorders_list, sellorders_list]

# https://tradeogre.com/api/v1/orders/BTC-SCP
def get_to_orders():
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
    return [buy_orders_list, sell_orders_list]

def combine_data(data):
    combined_buys = []
    combined_sells = []
    for e in data:
        for order in e[0]:
            combined_buys.append(order)
        for order in e[1]:
            combined_sells.append(order)
    combined_buys = sorted(combined_buys, key=itemgetter(4), reverse=True)
    combined_sells = sorted(combined_sells, key=itemgetter(4), reverse=True)
    return [combined_buys, combined_sells]

def main():
    x = combine_data([get_to_orders(), get_sx_orders('https://www.southxchange.com/api/book/SCP/BTC')])
    for e in x[1][-10:]:
        print(e)
    print()
    for e in x[0][0:10]:
        print(e)
    

if __name__ == "__main__":
    main()