from flask import render_template, Response, request
from app import app
import pumpthecoin
import spf_earnings


@app.route('/', methods=['GET'])
@app.route('/pumpthecoin', methods=['GET', 'POST'])
def pump_the_coin():
        if request.method == 'GET':
                return render_template('index.html', pumpthecoin_data=[0])
        elif request.method == 'POST':
                pump_the_coin = [0, 0, 0, 0, 0]
                combine = []
                if 'SXBTC' in request.form.getlist('market'):
                        pump_the_coin[0] = 1
                        combine.append(pumpthecoin.get_sx_orders('https://www.southxchange.com/api/book/SCP/BTC'))
                if 'TOBTC' in request.form.getlist('market'):
                        pump_the_coin[1] = 1
                        combine.append(pumpthecoin.get_to_orders())
                data = pumpthecoin.combine_data(combine)
                if request.form['Price'] != '':
                        amount = 0
                        for e in data[1]:
                                while float(e[4]) < float(request.form['Price']):
                                        amount += e[2]
                                else:
                                        amount += 1
                        pump_the_coin[2] = amount
                elif request.form['amountToBuy'] != '':
                        pump_the_coin[3] = request.form['amountToBuy']
                elif request.form['amountToSell'] != '':
                        pump_the_coin[4] = request.form['amountToSell']
                return render_template('index.html', pumpthecoin_data=data)

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
        if request.method == 'GET':
                return render_template('index.html', spf_data = spf_earnings.earnings(10000, 1, 'no_data'))
        elif request.method == 'POST':
                if request.form['SPFamount'] == '':
                        SPFamount = 10000
                else:
                        SPFamount = float(request.form['SPFamount'])
                if request.form['numberOfMonths'] == '':
                        numberOfMonths = 1
                else:
                        numberOfMonths = float(request.form['numberOfMonths'])
                if request.form['dataStored'] == '':
                        dataStored = 'no_data'
                else:
                        dataStored = float(request.form['dataStored'])
                return render_template('index.html', spf_data = spf_earnings.earnings(SPFamount, numberOfMonths, dataStored))
