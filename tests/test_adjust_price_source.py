import unittest
import datetime
import requests
from unittest.mock import patch
from app.finfo import PriceAdjustSource


class PriceAdjustSourceTest(unittest.TestCase):
    def setUp(self):
        self._get = requests.get
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

    @patch('requests.get')
    def test_get_adjust_today_when_finfo_fail(self, request_get_mock):
        res = requests.Response()
        res.status_code = 400
        request_get_mock.return_value = res

        self.assertRaises(RuntimeError, self._source.get_today_adjust)

    def test_get_adjust_today_when_call_twice_should_cache(self):
        adjusts = self._source.get_today_adjust()
        self.assertTrue(len(adjusts) > 0)
        if len(adjusts) > 0:
            for ad in adjusts:
                self.validate_adjust_info(ad)
        get_method = requests.get
        with patch('requests.get', wraps=get_method) as get_mock:
            adjusts = self._source.get_today_adjust()
            self.assertTrue(len(adjusts) > 0)
            if len(adjusts) > 0:
                for ad in adjusts:
                    self.validate_adjust_info(ad)
            call_args_list = get_mock.call_args_list
            self.assertEqual(0, len(call_args_list))

