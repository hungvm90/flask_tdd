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


class PriceAdjustSource(object):
    def __init__(self, url):
        self._url = url

    def get_today_adjust(self):
        return []