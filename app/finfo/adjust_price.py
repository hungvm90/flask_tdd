import json


class AdjustInfo(object):
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

    def get_today_adjust(self):
        return []
