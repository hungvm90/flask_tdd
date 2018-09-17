from app.finfo import PriceAdjustSource
from app.stockbook import Api
from app.log import AdjustLog


class AdjustPriceService(object):
    def __init__(self):
        self._source = None
        self._stockbook_api = None
        self._log = None

    def adjust_price_for_symbol(self, ad):
        adjusted_log = self._log.get_logs()
        if ad not in adjusted_log:
            print(self._stockbook_api.adjust_price)
            if self._stockbook_api.adjust_price(symbol=ad.symbol, ratio=ad.ratio):
                self._log.log(adjust_price=ad)
                return True
        return False

    def adjust_for_today(self):
        adjusts = self._source.get_today_adjust()
        adjusted = []
        for ad in adjusts:
            if self.adjust_price_for_symbol(ad):
                adjusted.append(ad)
        return adjusted

    def init(self, app):
        self._source = PriceAdjustSource(app.config['PRICE_ADJUST_SOURCE_URL'])
        self._stockbook_api = Api(app.config['STOCKBOOK_API'])
        self._log = AdjustLog(app.config['DATA_FILE'])