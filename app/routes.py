from flask import render_template, Response
from app import app
import pumpthecoin
import spf_earnings


@app.route('/', methods=['GET'])
@app.route('/all', methods=['GET'])
def all():
        data = pumpthecoin.combine_data([pumpthecoin.get_to_orders(), pumpthecoin.get_sx_orders('https://www.southxchange.com/api/book/SCP/BTC'), pumpthecoin.get_sx_orders('https://www.southxchange.com/api/book/SCP/USDT'), pumpthecoin.get_sx_orders('https://www.southxchange.com/api/book/SCP/ETH'), pumpthecoin.get_sx_orders('https://www.southxchange.com/api/book/SCP/LTC')])
        sell_orders = data[1][-10:]
        buy_orders = data[0][0:10]
        return render_template('index.html', data_to=[buy_orders, sell_orders])

@app.route('/southxchange', methods=['GET'])
def southxchange():
        data = pumpthecoin.combine_data([pumpthecoin.get_sx_orders('https://www.southxchange.com/api/book/SCP/BTC'), pumpthecoin.get_sx_orders('https://www.southxchange.com/api/book/SCP/USDT'), pumpthecoin.get_sx_orders('https://www.southxchange.com/api/book/SCP/ETH'), pumpthecoin.get_sx_orders('https://www.southxchange.com/api/book/SCP/LTC')])
        sell_orders = data[1][-10:]
        buy_orders = data[0][0:10]
        return render_template('index.html', data_to=[buy_orders, sell_orders])

@app.route('/trade_ogre', methods=['GET'])
def trade_ogre():
        data = pumpthecoin.combine_data([pumpthecoin.get_to_orders()])
        sell_orders = data[1][-10:]
        buy_orders = data[0][0:10]
        return render_template('index.html', data_to=[buy_orders, sell_orders])

@app.route('/stats/to', methods=['GET'])
def stats_to():
        return render_template('index.html', grouped_data = pumpthecoin.group_to_orders())

@app.route('/uptimerobot', methods=['GET'])
def uptimerobot():
        return Response("{'Success'='True}", status=200, mimetype='application/json')

@app.route('/spf_earnings', methods=['GET', 'POST'])
def spfearnings():
        return render_template('index.html', spf_data = spf_earnings.earnings())
