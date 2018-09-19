import datetime
import requests
import json


class Api(object):
    def __init__(self, url, token):
        self._url = url
        self._token = token

    def adjust_price(self, symbol, ratio):
        headers = {
            'Authorization': self._token,
            'Content-Type': 'application/json'
        }
        data = {
            'stockCode': symbol,
            'adjustRatio': ratio,
            'applyTime': datetime.datetime.now().strftime('%Y-%m-%d')
        }
        res = requests.post(self._url + '/api/recommendation/adjust', json=data, headers=headers)
        if not res.ok:
            raise RuntimeError(json.dumps(res.text))
