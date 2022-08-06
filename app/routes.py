from flask import render_template
from app import app
import pumpthecoin


@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
        return render_template('index.html')

@app.route('/api/<target_price>', methods=['GET'])
def response(target_price):
        btc, target, neccesary_amount, units = pumpthecoin.data(float(target_price))
        data = [btc, target, neccesary_amount, units]
        return render_template('index.html', data=data)