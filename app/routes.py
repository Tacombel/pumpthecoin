from flask import render_template, Response, request
from app import app
import pumpthecoin
import spf_earnings
import math
from operator import itemgetter
from time import time
from contest import get_balances, add_entry
from send_telegram import send_telegram_msg
import csv

def max_candle():
        with open('./contest/candles.csv') as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                line_count=0
                data = list(csv_reader)
                if len(data) < 2 :
                        return {"success":False, "error": "csv lenght < 2"}
                candles = []
                for row in data:
                        if line_count == 0:
                                line_count += 1
                        else:
                                candles.append(float(row[1]))
                return {"success":True, "max_candle": max(candles)}

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
                if 'SXBTC' in request.form.getlist('market') or 'TOBTC' in request.form.getlist('market'):
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
                                pump_the_coin['error'] = 'You need to input data'        
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
                if 'SXBTC' in request.form.getlist('market') or 'TOBTC' in request.form.getlist('market') or 'SXUSDT' in request.form.getlist('market') or 'SXETH' in request.form.getlist('market') or 'SXLTC' in request.form.getlist('market'):
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
                        markets_data['error'] = 'You need to select at least one market'
                return render_template('index.html', markets=markets_data)

@app.route('/stats', methods=['GET', 'POST'])
def stats():
        if request.method == 'GET':
                return render_template('index.html', grouped_data=[0])
        elif request.method == 'POST':
                combine = []
                if 'SXBTC' in request.form.getlist('market') or 'TOBTC' in request.form.getlist('market'):
                        if 'SXBTC' in request.form.getlist('market'):
                                combine.append(pumpthecoin.get_sx_orders('https://www.southxchange.com/api/book/SCP/BTC'))
                        if 'TOBTC' in request.form.getlist('market'):
                                combine.append(pumpthecoin.get_to_orders())
                        data = pumpthecoin.combine_data(combine)
                        if 'SXBTC' in request.form.getlist('market') and 'TOBTC' in request.form.getlist('market'):
                                title=f'Data for SX-BTC and TO-BTC'
                        elif 'SXBTC' in request.form.getlist('market'):
                                title=f'Data for SX-BTC'
                        elif 'TOBTC' in request.form.getlist('market'):
                                title=f'Data for TO-BTC'
                        max_col = request.form['max_col']
                        group = {}
                        for order in data[0]:
                                key = str(math.trunc(float(order[3]) * 1E6))
                                if key in group:
                                        group[key] = group[key] + float(order[2])
                                else:
                                        group[key] = float(order[2])
                        total_in_bids =  int(round(sum(group.values()), 0))
                        bids_grouped = []
                        for key, value in group.items():
                                bids_grouped.append([f'From {int(key) * 100} to {int(key) * 100 + 99}', round(value, 0)])
                        bids_grouped.reverse()
                        max_b = max(bids_grouped, key=itemgetter(1))[1]
                        max_b = math.ceil(max_b / 10000) * 10000
                        group = {}
                        for order in data[1]:
                                key = str(math.trunc(float(order[3]) * 1E6))
                                if key in group:
                                        group[key] = group[key] + float(order[2])
                                else:
                                        group[key] = float(order[2])
                        total_in_asks = int(round(sum(group.values()), 0))
                        asks_grouped = []
                        for key, value in group.items():
                                asks_grouped.append([f'From {int(key) * 100} to {int(key) * 100 + 99}', round(value, 0)])
                        asks_grouped.reverse()
                        if max_col !='':
                                del asks_grouped[int(max_col):] 
                        max_a = max(asks_grouped, key=itemgetter(1))[1]
                        max_a = math.ceil(max_a / 10000) * 10000
                else:
                       return render_template('index.html', grouped_data={'error':'Select at least one market'}) 
                return render_template('index.html', title=title, max_b=max_b, max_a=max_a, grouped_data = [bids_grouped, asks_grouped, total_in_bids, total_in_asks])

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
        
@app.route('/contest', methods=['GET'])
def contest():
        contest_data = {}
        contest_data["lines"] = get_balances()
        candle = max_candle()
        if candle["success"] == True:
                contest_data["max_candle"] = candle["max_candle"]
        return render_template('index.html', contest_data = contest_data)
                
@app.route('/contest/add', methods=['POST'])
def contest_add():
        contest_data = {}
        if request.form["Nickname"] == '' or request.form["hash"] == '' or request.form["discord_user"] == '':
                contest_data["error"] = 'You need a Discord user, a nickname and a hash!!!!'
        else:
                entry = add_entry(request.form["discord_user"], request.form["Nickname"], request.form["hash"])
                send_telegram_msg(f'{request.form["discord_user"]}, under the nickname {request.form["Nickname"]}, joined the competition')
                if not entry["success"]:
                        contest_data["error"] = entry["error"]
                else:
                        contest_data["message"] = entry["message"]
        contest_data["lines"] = get_balances()
        return render_template('index.html', contest_data = contest_data)

@app.route('/contest/candle', methods=['POST'])
def contest_candle():
        contest_data = {}
        if request.form["discord_user"] == '' or request.form["amount"] == '' or request.form["date"] == '':
                contest_data["error"] = 'You need a Discord user, amount and a date!!!!'
        else:
                msg = f'{request.form["discord_user"]} reported a candle of {request.form["amount"]} scp, the {request.form["date"]}'
                send_telegram_msg(msg)
                contest_data["message"] = str(f'{request.form["discord_user"]}, you reported succesfully')
                try:
                        with open('./contest/candles.csv', mode='r') as csv_file:
                                pass
                except FileNotFoundError:
                         with open('./contest/candles.csv', mode='w') as csv_file:
                                fieldnames = ['discord_user', 'amount', 'date']
                                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                                writer.writeheader()
                with open('./contest/candles.csv', mode='a') as csv_file:
                        fieldnames = ['discord_user', 'amount', 'date']
                        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                        writer.writerow({"discord_user": request.form["discord_user"], "amount": request.form["amount"], "date": request.form["date"]})
        contest_data["lines"] = get_balances()
        return render_template('index.html', contest_data = contest_data)

@app.route('/contest/rules', methods=['GET'])
def contest_rules():
        return render_template('rules.html')