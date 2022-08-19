from logging import PlaceHolder
import requests
import json
import sys


def btc_price():
    btc = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd')
    btc = btc.json()
    btc = btc['bitcoin']['usd']
    return btc

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
    return btc, target, neccesary_amount, units

def global_data():
    # total coins in circulation
    data = requests.get('https://consensus.scpri.me/status')
    total_coins = data.json()['totalcoins']
    #data from southxchange
    purgue_data_factor = 99.9
    data = requests.get('https://www.southxchange.com/api/book/SCP/BTC')
    sellorders = data.json()['SellOrders']
    buyorders = data.json()['BuyOrders']
    units_in_sellorders_total = 0
    #sell orders
    for e in sellorders:
        units_in_sellorders_total += float(e['Amount'])
    units_to_consider = units_in_sellorders_total * purgue_data_factor / 100
    units_in_sellorders = 0
    btc_in_sellorders = 0
    for e in sellorders:
        units_in_sellorders += float(e['Amount'])
        if units_in_sellorders > units_to_consider:
            units_in_sellorders -= float(e['Amount'])
            break
        btc_in_sellorders += float(e['Amount']) * float(e['Price'])
    #buy orders
    units_in_buyorders = 0
    btc_in_buyorders = 0
    for e in buyorders:
        units_in_buyorders += float(e['Amount'])
        btc_in_buyorders += float(e['Amount']) * float(e['Price'])
    response = {'units_in_sell_orders': units_in_sellorders, 'btc_in_sellorders': btc_in_sellorders, 'units_in_buyorders': units_in_buyorders, 'btc_in_buyorders': btc_in_buyorders, 'units_in_sellorders_total': units_in_sellorders_total, 'total_coins': total_coins}
    
    return response

if __name__ == "__main__":
    for index, e in enumerate(sys.argv):
        if index == 0:
            continue
        if e == 'e':
            data = global_data()
            btc = btc_price()
            print(f'Data from Southxchange API for the pair spc/BTC only.')
            print()
            print(f'There are a total of {data["units_in_sellorders_total"]:.2f} coins in sell orders. This is {data["units_in_sellorders_total"] / data["total_coins"] * 100:.2f}% of the current coin in circulation.')
            print(f'We will only consider {data["units_in_sell_orders"] / data["units_in_sellorders_total"] * 100:.2f}% of the coins to minimize distortions. That leaves {data["units_in_sell_orders"]:.2f} coins in sell orders.')
            print(f'The total asking price is {data["btc_in_sellorders"]:.2f} btc and the average is ${data["btc_in_sellorders"] / data["units_in_sell_orders"] * btc:.2f}/spc')
            print()
            print(f'There are {data["units_in_buyorders"]:.2f} coins in buy orders. This is {data["units_in_buyorders"] / data["total_coins"] * 100:.2f}% of the current coin in circulation.')
            print(f'The total asking price is {data["btc_in_buyorders"]:.2f} btc')
            print(f'The average asking price is ${data["btc_in_buyorders"] / data["units_in_buyorders"] * btc:.2f}')
        else:
            target_price = float(e)
            btc, target, neccesary_amount, units = data(target_price)
            print(f'What do I need to take scp to ${target_price}?')
            print(f'Bitcoin is now at ${btc}')
            print(f'I will have to buy all sell orders up to {target} btc')
            print(f'I need {neccesary_amount:.2f} btc or, in dollars, ${neccesary_amount * btc:.0f} plus commissions')
            print(f'I will end having {units:.2f} coins at an average price of ${neccesary_amount * btc / units:.2f}')
        continue
