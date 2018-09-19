import unittest
import datetime
import requests
from unittest.mock import patch
from app.stockbook import Api


class StockbookApiTest(unittest.TestCase):
    def setUp(self):
        self.token = ''
        self.url = 'https://stockbookapi-uat.vndirect.com.vn'
        self._api = Api(self.url, self.token)

    def tearDown(self):
        pass

    @patch('requests.post')
    def test_call_api_when_success(self, request_post_mock):
        stock_code = "ACBXX"
        ratio = 0.975
        res = requests.Response()
        res.status_code = 200
        request_post_mock.return_value = res
        data = {
            'stockCode': stock_code,
            'adjustRatio': ratio,
            'applyTime': datetime.datetime.now().strftime('%Y-%m-%d')
        }
        headers = {
            'Authorization': self.token,
            'Content-Type': 'application/json'
        }

        self._api.adjust_price(stock_code, ratio)

        call_args_list = request_post_mock.call_args_list
        self.assertEqual(1, len(call_args_list))
        (args, kwargs) = call_args_list[0]
        self.assertEqual(self.url + '/api/recommendation/adjust', args[0])
        request_data = kwargs.get('json', {})
        request_headers = kwargs.get('headers', {})
        self.assertEqual(data, request_data)
        self.assertEqual(headers, request_headers)

    @patch('requests.post')
    def test_call_api_when_fail_should_throw_exception(self, request_post_mock):
        stock_code = "ACBXX"
        ratio = 0.975
        res = requests.Response()
        res.status_code = 400
        request_post_mock.return_value = res
        data = {
            'stockCode': stock_code,
            'adjustRatio': ratio,
            'applyTime': datetime.datetime.now().strftime('%Y-%m-%d')
        }
        headers = {
            'Authorization': self.token,
            'Content-Type': 'application/json'
        }

        # is_ok = self._api.adjust_price("ACB", 0.975)
        with self.assertRaises(RuntimeError):
            self._api.adjust_price(stock_code, ratio)

        call_args_list = request_post_mock.call_args_list
        self.assertEqual(1, len(call_args_list))
        (args, kwargs) = call_args_list[0]
        self.assertEqual(self.url + '/api/recommendation/adjust', args[0])
        request_data = kwargs.get('json', {})
        request_headers = kwargs.get('headers', {})
        self.assertEqual(data, request_data)
        self.assertEqual(headers, request_headers)

