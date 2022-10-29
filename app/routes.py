from flask import render_template
from app import app
import pumpthecoin


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
