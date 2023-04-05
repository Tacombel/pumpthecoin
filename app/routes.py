from flask import render_template, Response, request
from app import app
import pumpthecoin
import spf_earnings

@app.route('/uptimerobot', methods=['GET'])
def uptimerobot():
        return Response("{'Success'='True}", status=200, mimetype='application/json')

@app.route('/', methods=['GET'])
@app.route('/pumpthecoin', methods=['GET', 'POST'])
def pump_the_coin():
        if request.method == 'GET':
                return render_template('index.html', pumpthecoin_data=[0])
        elif request.method == 'POST':
                pump_the_coin = {}
                combine = []
                if 'SXBTC' or 'TOBTC' in request.form.getlist('market'):
                        if 'SXBTC' in request.form.getlist('market'):
                                combine.append(pumpthecoin.get_sx_orders('https://www.southxchange.com/api/book/SCP/BTC'))
                        if 'TOBTC' in request.form.getlist('market'):
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
                                        pump_the_coin['last_price'] = round(ask[-1][4], 4)
                                pump_the_coin['dollars'] = round(dollars)
                                pump_the_coin['amount'] = round(amount)
                                pump_the_coin['average'] = round(dollars / amount, 4)
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
                                                break
                                        order += 1
                                pump_the_coin['amount_buying'] = round(float(request.form['amountToBuy']))
                                if order > len(ask):
                                        pump_the_coin['last_price_buying'] = round(ask[-1][4], 4) #used as key in the html
                                        pump_the_coin['amount_buying'] = round(amount)
                                pump_the_coin['dollars_buying'] = round(dollars)
                                pump_the_coin['average_buying'] = round(dollars / float(request.form['amountToBuy']), 2)
                        elif request.form['amountToSell'] != '':
                                bid = data[0]
                                dollars = 0
                                amount = 0
                                order = 1
                                for e in bid:
                                        if amount + e[2] < float(request.form['amountToSell']):
                                                dollars += e[5]
                                                amount += e[2]
                                        else:
                                                rest = float(request.form['amountToSell']) - amount
                                                amount += rest
                                                dollars += rest * e[4]
                                                break
                                        order += 1
                                pump_the_coin['amount_selling'] = round(float(request.form['amountToSell']))
                                if order > len(bid):
                                        pump_the_coin['last_price_selling'] = round(ask[-1][4], 4) #used as key in the html
                                        pump_the_coin['amount_selling'] = round(amount)
                                pump_the_coin['dollars_selling'] = round(dollars)
                                pump_the_coin['average_selling'] = round(dollars / float(request.form['amountToSell']), 2)
                else:
                        pump_the_coin['error'] = 'You need to select at least one market'
                return render_template('index.html', pumpthecoin_data=pump_the_coin)

@app.route('/markets', methods=['GET', 'POST'])
def markets():
        if request.method == 'GET':
                return render_template('index.html', markets=[0])
        elif request.method == 'POST':
                markets_data = {}
                combine = []
                if 'SXBTC' or 'TOBTC' or 'SXUSDT' or 'SXETH' or 'SXLTC' in request.form.getlist('market'):
                        if 'SXBTC' in request.form.getlist('market'):
                                combine.append(pumpthecoin.get_sx_orders('https://www.southxchange.com/api/book/SCP/BTC'))
                        if 'SXUSDT' in request.form.getlist('market'):
                                combine.append(pumpthecoin.get_sx_orders('https://www.southxchange.com/api/book/SCP/USDT'))
                        if 'SXETH' in request.form.getlist('market'):
                                combine.append(pumpthecoin.get_sx_orders('https://www.southxchange.com/api/book/SCP/ETH'))
                        if 'SXLTC' in request.form.getlist('market'):
                                combine.append(pumpthecoin.get_sx_orders('https://www.southxchange.com/api/book/SCP/LTC'))
                        if 'TOBTC' in request.form.getlist('market'):
                                combine.append(pumpthecoin.get_to_orders())
                        data = pumpthecoin.combine_data(combine)
                        markets_data['sell_orders'] = data[1][-10:]
                        markets_data['buy_orders'] = data[0][0:10]
                else:
                        markets['error'] = 'You need to select at least one market'
                return render_template('index.html', markets=markets_data)

@app.route('/stats/to', methods=['GET'])
def stats_to():
        return render_template('index.html', grouped_data = pumpthecoin.group_to_orders())

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
