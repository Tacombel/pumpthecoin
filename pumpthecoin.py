from importlib.util import find_spec
import requests
import sys
from config import Config
from operator import itemgetter


def btc_price():
    btc = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd')
    btc = btc.json()
    btc = float(btc['bitcoin']['usd'])
    return btc

def spc_price():
    spc = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=siaprime-coin&vs_currencies=btc%2Cusd')
    spc = spc.json()
    spc = spc['siaprime-coin']['usd']
    return spc

def usdt_price():
    usdt = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=tether&vs_currencies=usd')
    usdt = usdt.json()
    usdt = usdt['tether']['usd']
    return usdt

def eth_price():
    eth = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd')
    eth = eth.json()
    eth = eth['ethereum']['usd']
    return eth

def ltc_price():
    ltc = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=litecoin&vs_currencies=usd')
    ltc = ltc.json()
    ltc = ltc['litecoin']['usd']
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

def get_orders(books): #books is a list of API addresses
    buy_orders = []
    sell_orders = []
    for e in books:
        type = e.split('/')[6]
        if type == 'BTC':
            price = btc_price()
        elif type == 'USDT':
            price = usdt_price()
        elif type == 'LTC':
            price = ltc_price()
        elif type == 'ETH':
            price = eth_price()
        data = requests.get(e)
        sellorders = data.json()['SellOrders']
        buyorders = data.json()['BuyOrders']
        for order in sellorders:
            del order['Index']
            order['Price'] = order['Price'] * price
            order['Book'] = type
            order['Value'] = order['Amount'] * order['Price']
            sell_orders.append(order)
        for order in buyorders:
            del order['Index']
            order['Price'] = order['Price'] * price
            order['Book'] = type
            order['Value'] = order['Amount'] * order['Price']
            buy_orders.append(order)
    buy_orders = sorted(buy_orders, key=itemgetter('Price'), reverse=True)
    sell_orders = sorted(sell_orders, key=itemgetter('Price'), reverse=False)
    return buy_orders, sell_orders


def global_data(books):
    # total coins in circulation
    data = requests.get('https://consensus.scpri.me/status')
    total_coins = data.json()['totalcoins']
    buyorders, sellorders = get_orders(books)
    units_in_sellorders_total = 0
    #sell orders
    for e in sellorders:
        units_in_sellorders_total += float(e['Amount'])
    units_in_sellorders = 0
    dollars_in_sellorders = 0
    first_order = True
    for e in sellorders:
        if not first_order and (float(e['Price'] > (dollars_in_sellorders / units_in_sellorders * Config.discard_factor))):
            break
        units_in_sellorders += float(e['Amount'])
        dollars_in_sellorders += float(e['Amount']) * float(e['Price'])
        first_order = False
        last_price_considered = float(e['Price'])
    #buy orders
    units_in_buyorders = 0
    dollars_in_buyorders = 0
    for e in buyorders:
        units_in_buyorders += float(e['Amount'])
        dollars_in_buyorders += float(e['Amount']) * float(e['Price'])
    response = {'units_in_sell_orders': units_in_sellorders, '$_in_sellorders': dollars_in_sellorders, 'units_in_buyorders': units_in_buyorders, '$_in_buyorders': dollars_in_buyorders, 'units_in_sellorders_total': units_in_sellorders_total, 'total_coins': total_coins, 'last_price_considered': last_price_considered, 'discard_factor': Config.discard_factor, 'price_spc_usd': spc_price(), 'price_btc_usd': btc_price(), 'price_eth_usd': eth_price(), 'price_ltc_usd': ltc_price(), 'sell_first_orders': reversed(sellorders[:Config.orders_listed]), 'buy_first_orders': buyorders[:Config.orders_listed], 'gap': ((sellorders[0]['Price'] - buyorders[0]['Price']) / buyorders[0]['Price'] * 100)}
    
    return response

if __name__ == "__main__":
    # Pasar e como argumento para resumen del mercado o una cifra para pumpthecoin
    for index, e in enumerate(sys.argv):
        if index == 0:
            continue
        if e == 'e':
            # data from southxchange
            # 'https://www.southxchange.com/api/book/SCP/BTC', 'https://www.southxchange.com/api/book/SCP/USDT', 'https://www.southxchange.com/api/book/SCP/ETH', 'https://www.southxchange.com/api/book/SCP/LTC'
            books = ['https://www.southxchange.com/api/book/SCP/BTC', 'https://www.southxchange.com/api/book/SCP/USDT', 'https://www.southxchange.com/api/book/SCP/ETH', 'https://www.southxchange.com/api/book/SCP/LTC']
            print(books)
            data = global_data(['https://www.southxchange.com/api/book/SCP/BTC', 'https://www.southxchange.com/api/book/SCP/USDT', 'https://www.southxchange.com/api/book/SCP/ETH', 'https://www.southxchange.com/api/book/SCP/LTC'])
            print()
            print(data)
            print()
            btc = btc_price()
            print()
            print('SELL ORDERS')
            print(f'There are a total of {data["units_in_sellorders_total"]:.2f} coins (${data["units_in_sellorders_total"] * data["price_spc_usd"]:.2f}) in sell orders. This is {data["units_in_sellorders_total"] / data["total_coins"] * 100:.2f}% of the current coin in circulation.')
            print(f'To avoid distortion from orders with prices well above the rest, we will discard all remaining orders if the price of the order being considered is {data["discard_factor"]} times above the current average.')
            print(f'The price at which we stopped considering orders is ${data["last_price_considered"]:.2f}.')
            print(f'We will consider {data["units_in_sell_orders"] / data["units_in_sellorders_total"] * 100:.2f}% of the coins at the exchange. That is {data["units_in_sell_orders"]:.2f} coins in sell orders.')
            print(f'The total asking price is ${data["$_in_sellorders"]:.2f} and the average is ${data["$_in_sellorders"] / data["units_in_sell_orders"]:.2f}/spc')
            print()
            for e in data['sell_first_orders']:
                print(e)
            print(f'Gap: {data["gap"]:.2f}%')
            print('BUY ORDERS')
            for e in data['buy_first_orders']:
                print(e)
            print()
            print(f'There are {data["units_in_buyorders"]:.2f} coins in buy orders. This is {data["units_in_buyorders"] / data["total_coins"] * 100:.2f}% of the current coin in circulation.')
            print(f'The total asking price is ${data["$_in_buyorders"]:.2f}')
            print(f'The average asking price is ${data["$_in_buyorders"] / data["units_in_buyorders"]:.2f}')
        else:
            target_price = float(e)
            btc, target, neccesary_amount, units = data(target_price)
            print(f'What do I need to take scp to ${target_price}?')
            print(f'Bitcoin is now at ${btc}')
            print(f'I will have to buy all sell orders up to {target} btc')
            print(f'I need {neccesary_amount:.2f} btc or, in dollars, ${neccesary_amount * btc:.0f} plus commissions')
            print(f'I will end having {units:.2f} coins at an average price of ${neccesary_amount * btc / units:.2f}')
        continue
