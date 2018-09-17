import unittest
import json
import datetime
from app.finfo import PriceAdjustSource


class PriceAdjustSourceTest(unittest.TestCase):
    def setUp(self):
        self._source = PriceAdjustSource('https://finfo-api.vndirect.com.vn/v3/stocks/adjustRatio')

    def tearDown(self):
        pass

    def validate_adjust_info(self, ad):
        self.assertTrue(0 < ad.ratio < 1)
        now = datetime.datetime.now()
        datetime_object = datetime.datetime.strptime(ad.date, '%Y-%m-%dT%H:%M:%S')
        self.assertTrue(now.date() == datetime_object.date())

    def test_get_adjust_today(self):
        adjusts = self._source.get_today_adjust()
        self.assertTrue(len(adjusts) > 0)
        if len(adjusts) > 0:
            for ad in adjusts:
                self.validate_adjust_info(ad)
