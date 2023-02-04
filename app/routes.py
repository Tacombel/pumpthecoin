from flask import render_template
from app import app
import pumpthecoin
import to


@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
        return render_template('index.html', data_global=pumpthecoin.global_data(['https://www.southxchange.com/api/book/SCP/BTC', 'https://www.southxchange.com/api/book/SCP/USDT', 'https://www.southxchange.com/api/book/SCP/ETH', 'https://www.southxchange.com/api/book/SCP/LTC']))

@app.route('/pump/<target_price>', methods=['GET'])
def response(target_price):
        target_price = float(target_price)
        btc, target, neccesary_amount, units = pumpthecoin.data(target_price)
        data = [btc, target, neccesary_amount, units]
        return render_template('index.html', data=data, target_price=target_price)

@app.route('/trade_ogre', methods=['GET'])
def trade_ogre():
        price = pumpthecoin.btc_price()
        data=to.get_order_book()
        sell_orders = data[0]
        sell_orders = sell_orders[-5:]
        buy_orders = data[1]
        buy_orders = buy_orders[0:5]
        for e in sell_orders:
                e.append(float(e[0]) * price)
                e.append(float(e[0]) * float(e[1]) * price)
        for e in buy_orders:
                e.append(float(e[0]) * price)
                e.append(float(e[0]) * float(e[1]) * price)
        return render_template('index.html', data_to=[reversed(sell_orders), reversed(buy_orders)])