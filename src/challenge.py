import requests
import json
import urllib.request, urllib.parse, urllib.error
import os
import datetime
from flask import Flask, request

app = Flask(__name__)

apikey = os.environ.get('API_KEY')

@app.route('/', methods=['GET'])
def home():
    return '''<h1>Prototype API<h1><p>Returns average stock prices for given number of days</p.'''

@app.route('/api/v1/resources/stock', methods=['GET'])
def stock():
    # look for two request params:
    ndays = int(request.args.get('ndays'))
    symbol = request.args.get('symbol')

    if not (ndays or symbol):
        return "Error in args"

    # build the upstream request URI:
    getVars = {}
    getVars['apikey'] = apikey
    getVars['function'] = "TIME_SERIES_DAILY_ADJUSTED"
    getVars['symbol'] = symbol
    base_url = "https://www.alphavantage.co/query?"

    url = (base_url + urllib.parse.urlencode(getVars))

    # go get the API response:
    response = requests.get(url)

    # put the JSON in a dict:
    data = response.json()

    # Build a list of the last 4 days closing prices.
    prices = []

    while ndays > 0:
        # This relies on Python3 ordering the JSON dict:
        key = list(data['Time Series (Daily)'])[ndays - 1]
        prices.append(round(float(data['Time Series (Daily)'][key]['4. close']), 2))
        ndays -= 1

    # simple average:
    avg = float(sum(prices) / len(prices))

    # sample return:
    # MSFT data=[110.56, 111.25, 115.78], average=112.50

    message = symbol + " data=" + str(prices) + ", average=" + str(round(avg,2))

    return message

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
