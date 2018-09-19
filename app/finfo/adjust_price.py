import json
import requests
import datetime


class AdjustInfo:
    def __init__(self, symbol, ratio, date):
        self._symbol = symbol
        self._ratio = ratio
        self._date = date

    @property
    def symbol(self):
        return self._symbol

    @property
    def ratio(self):
        return self._ratio

    @property
    def date(self):
        return self._date

    def __str__(self) -> str:
        return json.dumps(self.to_json())

    def __repr__(self) -> str:
        return self.__str__()

    def __eq__(self, o: object) -> bool:
        if isinstance(o, AdjustInfo):
            return self is o or (self._symbol == o._symbol and self._ratio == o._ratio and self._date == o._date)

    def to_json(self):
        json_adjust_info = {
            'symbol': self._symbol,
            'ratio': self._ratio,
            'date': self._date
        }
        return json_adjust_info

    @staticmethod
    def from_json(json_adjust_info):
        return AdjustInfo(symbol=json_adjust_info.get('symbol'), ratio=json_adjust_info.get('ratio'),
                          date=json_adjust_info.get('date'))


class PriceAdjustSource(object):
    def __init__(self, url):
        self._url = url
        self._cache = {}

    @staticmethod
    def is_today(s):
        datetime_object = datetime.datetime.strptime(s, '%Y-%m-%dT%H:%M:%S')
        today = datetime.datetime.today()
        return datetime_object.date() == today.date()

    def get_today_adjust(self):
        today = datetime.datetime.now().strftime('%Y-%m-%d')
        if self._cache.get(today) is not None:
            return self._cache.get(today)
        res = requests.get("{}?fromDate={}".format(self._url, today),
                           timeout=3)
        if res.ok:
            today_adjusts = []
            data = res.json()
            data = data.get('data', {})
            hits = data.get('hits', [])
            for hit in hits:
                _source = hit['_source']
                ad_info = AdjustInfo(_source['symbol'], _source['adjustRatio'], _source['adjustDate'])
                if self.is_today(ad_info.date):
                    today_adjusts.append(ad_info)
            self._cache[today] = today_adjusts
            return today_adjusts
        else:
            raise RuntimeError("error: " + res.text)
