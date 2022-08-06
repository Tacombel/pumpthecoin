import requests
import json
import sys

def data(target_price):
    btc = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd')
    btc = btc.json()
    btc = btc['bitcoin']['usd']
    target = target_price / btc
    data = requests.get('https://www.southxchange.com/api/book/SCP/BTC')
    data = data.json()['SellOrders']
    neccesary_amount = 0
    units = 0
    for e in data:
        if float(e['Price']) < target:
            neccesary_amount += float(e['Amount']) * float(e['Price'])
            units += float(e['Amount'])
    return btc, target, neccesary_amount, units


if __name__ == "__main__":
    for index, e in enumerate(sys.argv):
        if index == 0:
            continue
        target_price = float(e)
        continue

    btc, target, neccesary_amount, units = data(target_price)
    print(f'What do I need to take scp to ${target_price}?')
    print(f'Bitcoin is now at ${btc}')
    print(f'I will have to buy all sell orders up to {target} btc')
    print(f'I need {neccesary_amount:.2f} btc or, in dollars, ${neccesary_amount * btc:.0f} plus commissions')
    print(f'I will end having {units:.2f} coins at an average price of ${neccesary_amount * btc / units:.2f}')
