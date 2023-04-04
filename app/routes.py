from flask import render_template, Response, request
from app import app
import pumpthecoin
import spf_earnings
import logging


@app.route('/', methods=['GET'])
@app.route('/pumpthecoin', methods=['GET', 'POST'])
def pump_the_coin():
        if request.method == 'GET':
                return render_template('index.html', pumpthecoin_data=[0])
        elif request.method == 'POST':
                pump_the_coin = {}
                combine = []
                if 'SXBTC' in request.form.getlist('market'):
                        pump_the_coin[0] = 1
                        combine.append(pumpthecoin.get_sx_orders('https://www.southxchange.com/api/book/SCP/BTC'))
                if 'TOBTC' in request.form.getlist('market'):
                        pump_the_coin[1] = 1
                        combine.append(pumpthecoin.get_to_orders())
                data = pumpthecoin.combine_data(combine)
                ask = data[1]
                ask.reverse()
                if request.form['Price'] != '':
                        pump_the_coin['price'] = float(request.form['Price'])
                        dollars = 0
                        amount = 0
                        order = 1
                        for e in ask:
                                if float(e[4]) < float(request.form['Price']):
                                        dollars += e[5]
                                        amount += e[2]
                                else:
                                        break
                                order += 1
                        if order > len(ask):
                                pump_the_coin['last_price'] = ask[-1][4]
                        pump_the_coin['dollars'] = round(dollars)
                        pump_the_coin['amount'] = round(amount)
                elif request.form['amountToBuy'] != '':
                        dollars = 0
                        amount = 0
                        order = 1
                        for e in ask:
                                if amount + e[2] < float(request.form['amountToBuy']):
                                        dollars += e[5]
                                        amount += e[2]
                                else:
                                        rest = float(request.form['amountToBuy']) - amount
                                        amount += rest
                                        dollars += rest * e[4]
                                        print(f'else {amount} {dollars}')
                                        break
                                order += 1
                        pump_the_coin['amount_buying'] = round(float(request.form['amountToBuy']))
                        if order > len(ask):
                                pump_the_coin['last_price_buying'] = ask[-1][4]
                                pump_the_coin['amount_buying'] = round(amount)
                        pump_the_coin['dollars_buying'] = round(dollars)
                        pump_the_coin['average_buying'] = round(dollars / float(request.form['amountToBuy']), 2)
                elif request.form['amountToSell'] != '':
                        pump_the_coin['amountToSell'] = 'No way'
                return render_template('index.html', pumpthecoin_data=pump_the_coin)

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
