import requests
from operator import itemgetter
from time import time, sleep
import json
import math
import logging
import os

LOGLEVEL = os.environ.get('LOGLEVEL', 'DEBUG').upper()
logger = logging.getLogger(__name__)
c_handler = logging.StreamHandler()
c_handler.setLevel(LOGLEVEL)
c_format = logging.Formatter('%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
c_handler.setFormatter(c_format)
logger.addHandler(c_handler)
logger.info(f'LOGLEVEL: {LOGLEVEL}')

coingecko_queue = [0, 0, 0, 0, 0]
coingecko_timer = 60.0

price_btc_cg = 0
def btc_price():
    global coingecko_queue
    global price_btc_cg
    if time() > coingecko_queue[0] + coingecko_timer or price_btc_cg == 0:
        btc = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd')
        while True:
            if btc.status_code == 200:
                btc = btc.json()
                btc = float(btc['bitcoin']['usd'])
                price_btc_cg = btc
                del coingecko_queue[0]
                coingecko_queue.append(time())
                break
            else:
                logger.critical(f'Coingecko failed. Status code: {btc.status_code}. Retrying in 10 seconds')
                sleep(10)
    else:
        logger.debug(f'Using saved value')
        btc = price_btc_cg
    return btc

price_spc_cg = 0
def spc_price():
    global coingecko_queue
    global price_spc_cg
    if time() > coingecko_queue[0] + coingecko_timer or price_spc_cg == 0:
        spc = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=siaprime-coin&vs_currencies=btc%2Cusd')
        while True:
            if spc.status_code == 200:
                spc = spc.json()
                spc = spc['siaprime-coin']['usd']
                price_spc_cg = spc
                del coingecko_queue[0]
                coingecko_queue.append(time())
                break
            else:
                logger.critical(f'Coingecko failed. Status code: {spc.status_code}. Retrying in 10 seconds')
                sleep(10)
    else:
        logger.debug(f'Using saved value')
        spc = price_spc_cg
    return spc

price_usdt_cg = 0
def usdt_price():
    global coingecko_queue
    global price_usdt_cg
    if time() > coingecko_queue[0] + coingecko_timer or price_usdt_cg == 0:
        usdt = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=tether&vs_currencies=usd')
        while True:
            if usdt.status_code == 200:
                usdt = usdt.json()
                usdt = usdt['tether']['usd']
                price_usdt_cg = usdt
                del coingecko_queue[0]
                coingecko_queue.append(time())
                break
            else:
                logger.critical(f'Coingecko failed. Status code: {usdt.status_code}. Retrying in 10 seconds')
                sleep(10)
    else:
        logger.debug(f'Using saved value')
        usdt = price_usdt_cg
    return usdt

price_eth_cg = 0
def eth_price():
    global coingecko_queue
    global price_eth_cg
    if time() > coingecko_queue[0] + coingecko_timer or price_eth_cg == 0:
        eth = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd')
        while True:
            if eth.status_code == 200:
                eth = eth.json()
                eth = eth['ethereum']['usd']
                price_eth_cg = eth
                del coingecko_queue[0]
                coingecko_queue.append(time())
                break
            else:
                logger.critical(f'Coingecko failed. Status code: {eth.status_code}. Retrying in 10 seconds')
                sleep(10)
    else:
        logger.debug(f'Using saved value')
        eth = price_eth_cg
    return eth

price_ltc_cg = 0
def ltc_price():
    global coingecko_queue
    global price_ltc_cg
    if time() > coingecko_queue[0] + coingecko_timer or price_ltc_cg == 0:
        ltc = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=litecoin&vs_currencies=usd')
        ltc = ltc.json()
        ltc = ltc['litecoin']['usd']
        price_ltc_cg = ltc
        del coingecko_queue[0]
        coingecko_queue.append(time())
    else:
        logger.debug(f'Using saved value')
        ltc = price_ltc_cg
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
    while True:
        data = requests.get(book_url)
        if data.status_code == 200:
            break
        else:
            logger.critical(f'Error. Retrying {book_url} in 10 seconds')
            sleep(10)
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
    while True:
        orders = requests.get(url)
        if orders.status_code == 200:
            break
        else:
            logger.critical(f'Error. Retrying {url} in 10 seconds')
            sleep(10)
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

def group_to_orders():
    group = {}
    orders = get_to_orders()
    for order in orders[0]:
        key = str(math.trunc(float(order[3]) * 1E6))
        if key in group:
            group[key] = group[key] + float(order[2])
        else:
            group[key] = float(order[2])
    total_in_bids =  int(round(sum(group.values()), 0))
    bids_grouped = []
    for key, value in group.items():
        bids_grouped.append([f'From {int(key) * 100} to {int(key) * 100 + 99}', round(value, 0)])
    group = {}
    for order in orders[1]:
        key = str(math.trunc(float(order[3]) * 1E6))
        if key in group:
            group[key] = group[key] + float(order[2])
        else:
            group[key] = float(order[2])
    total_in_asks = int(round(sum(group.values()), 0))
    asks_grouped = []
    for key, value in group.items():
        asks_grouped.append([f'From {int(key) * 100} to {int(key) * 100 + 99}', round(value, 0)])
    return([bids_grouped, asks_grouped, total_in_bids, total_in_asks])

def main():
    x = combine_data([get_to_orders(), get_sx_orders('https://www.southxchange.com/api/book/SCP/BTC')])
    for e in x[1][-10:]:
        print(e)
    print()
    for e in x[0][0:10]:
        print(e)
    

if __name__ == "__main__":
    group_to_orders = group_to_orders()
    print(group_to_orders[0])
    print(group_to_orders[1])
    