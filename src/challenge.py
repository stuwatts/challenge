import requests
import json
import urllib.request, urllib.parse, urllib.error
import os
import datetime
from flask import Flask

app = Flask(__name__)

apikey = os.environ.get('API_KEY')
symbol = os.environ.get('SYMBOL')
ndays = int(os.environ.get('NDAYS'))

# build the upstream request URI:
getVars = {}
getVars['apikey'] = apikey
getVars['function'] = "TIME_SERIES_DAILY_ADJUSTED"
getVars['symbol'] = symbol
base_url = "https://www.alphavantage.co/query?"

url = (base_url + urllib.parse.urlencode(getVars))

@app.route('/')
def index():
    n = ndays
    # go get the API response:
    response = requests.get(url)

    # put the JSON in a dict:
    data = response.json()

    # Build a list of the last 4 days closing prices.
    prices = []

    while n > 0:
        # This relies on Python3 ordering the JSON dict:
        key = list(data['Time Series (Daily)'])[n - 1]
        prices.append(round(float(data['Time Series (Daily)'][key]['4. close']), 2))
        n -= 1

    # simple average:
    avg = float(sum(prices) / len(prices))

    # sample return:
    # MSFT data=[110.56, 111.25, 115.78], average=112.50

    message = symbol + " data=" + str(prices) + ", average=" + str(round(avg,2))

    return message

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
