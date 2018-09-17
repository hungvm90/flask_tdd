import unittest
import json
from unittest.mock import patch
import app
from app import create_app
from app.finfo import AdjustInfo
from app import AdjustPriceService


class AdjustPriceServiceTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        self.adjust_price_service = AdjustPriceService()
        self.adjust_price_service.init(self.app)

    def tearDown(self):
        self.app_context.pop()

    @patch.object(app.stockbook.Api, 'adjust_price', autospec=True)
    @patch.object(app.finfo.PriceAdjustSource, 'get_today_adjust', autospec=True)
    @patch.object(app.log.AdjustLog, 'log', autospec=True)
    @patch.object(app.log.AdjustLog, 'get_logs', autospec=True)
    def test_trigger_when_data_file_is_not_exist_should_create_logfile_and_add_success_adjust_log(self, get_logs_mock,
                                                                                                  log_mock,
                                                                                                  get_today_adjust_mock,
                                                                                                  adjust_price_mock):
        adjusts = []
        ad_acb = AdjustInfo("ACB", 0.98, "2018-09-14")
        adjusts.append(ad_acb)
        ad_vnd = AdjustInfo("VND", 0.88, "2018-09-14")
        adjusts.append(ad_vnd)
        get_today_adjust_mock.return_value = adjusts
        adjust_price_mock.return_value = True
        get_logs_mock.return_value = []

        adjusted = self.adjust_price_service.adjust_for_today()

        # then
        self.assertEqual(2, len(adjusted))
        self.assertIn(ad_acb, adjusted)
        self.assertIn(ad_vnd, adjusted)
        get_today_adjust_mock.assert_called_once()

        call_args_list = adjust_price_mock.call_args_list
        self.assertEqual(2, len(call_args_list))
        (args, kwargs) = call_args_list[0]
        self.assertEqual(ad_acb.symbol, kwargs['symbol'])
        self.assertEqual(ad_acb.ratio, kwargs['ratio'])
        (args, kwargs) = call_args_list[1]
        self.assertEqual(ad_vnd.symbol, kwargs['symbol'])
        self.assertEqual(ad_vnd.ratio, kwargs['ratio'])

        call_args_list = log_mock.call_args_list
        self.assertEqual(2, len(call_args_list))
        (args, kwargs) = call_args_list[0]
        self.assertEqual(ad_acb, kwargs['adjust_price'])
        (args, kwargs) = call_args_list[1]
        self.assertEqual(ad_vnd, kwargs['adjust_price'])

    @patch.object(app.stockbook.Api, 'adjust_price', autospec=True)
    @patch.object(app.finfo.PriceAdjustSource, 'get_today_adjust', autospec=True)
    @patch.object(app.log.AdjustLog, 'log', autospec=True)
    @patch.object(app.log.AdjustLog, 'get_logs', autospec=True)
    def test_trigger_when_data_file_is_not_exist_should_create_logfile_and_not_add_fail_adjust_log(self, get_logs_mock,
                                                                                                   log_mock,
                                                                                                   get_today_adjust_mock,
                                                                                                   adjust_price_mock):
        adjusts = []
        ad_acb = AdjustInfo("ACB", 0.98, "2018-09-14")
        adjusts.append(ad_acb)
        ad_vnd = AdjustInfo("VND", 0.88, "2018-09-14")
        adjusts.append(ad_vnd)
        get_today_adjust_mock.return_value = adjusts
        adjust_price_mock.side_effect = [True, False]
        get_logs_mock.return_value = []

        adjusted = self.adjust_price_service.adjust_for_today()

        # then
        self.assertEqual(1, len(adjusted))
        self.assertIn(ad_acb, adjusted)

        get_today_adjust_mock.assert_called_once()

        call_args_list = adjust_price_mock.call_args_list
        self.assertEqual(2, len(call_args_list))
        (args, kwargs) = call_args_list[0]
        self.assertEqual(ad_acb.symbol, kwargs['symbol'])
        self.assertEqual(ad_acb.ratio, kwargs['ratio'])
        (args, kwargs) = call_args_list[1]
        self.assertEqual(ad_vnd.symbol, kwargs['symbol'])
        self.assertEqual(ad_vnd.ratio, kwargs['ratio'])

        call_args_list = log_mock.call_args_list
        self.assertEqual(1, len(call_args_list))
        (args, kwargs) = call_args_list[0]
        self.assertEqual(ad_acb, kwargs['adjust_price'])

    @patch.object(app.stockbook.Api, 'adjust_price', autospec=True)
    @patch.object(app.finfo.PriceAdjustSource, 'get_today_adjust', autospec=True)
    @patch.object(app.log.AdjustLog, 'log', autospec=True)
    @patch.object(app.log.AdjustLog, 'get_logs', autospec=True)
    def test_trigger_when_adjusted_in_log_file_should_not_adjust(self, get_logs_mock,
                                                                 log_mock,
                                                                 get_today_adjust_mock,
                                                                 adjust_price_mock):
        adjusts = []
        ad_acb = AdjustInfo("ACB", 0.98, "2018-09-14")
        adjusts.append(ad_acb)
        ad_vnd = AdjustInfo("VND", 0.88, "2018-09-14")
        adjusts.append(ad_vnd)
        get_today_adjust_mock.return_value = adjusts
        adjust_price_mock.return_value = True
        get_logs_mock.return_value = [ad_acb]

        adjusted = self.adjust_price_service.adjust_for_today()

        # then
        self.assertEqual(1, len(adjusted))
        self.assertIn(ad_vnd, adjusted)

        get_today_adjust_mock.assert_called_once()

        call_args_list = adjust_price_mock.call_args_list
        self.assertEqual(1, len(call_args_list))
        (args, kwargs) = call_args_list[0]
        self.assertEqual(ad_vnd.symbol, kwargs['symbol'])
        self.assertEqual(ad_vnd.ratio, kwargs['ratio'])

        call_args_list = log_mock.call_args_list
        self.assertEqual(1, len(call_args_list))
        (args, kwargs) = call_args_list[0]
        self.assertEqual(ad_vnd, kwargs['adjust_price'])

    @patch.object(app.stockbook.Api, 'adjust_price', autospec=True)
    @patch.object(app.finfo.PriceAdjustSource, 'get_today_adjust', autospec=True)
    @patch.object(app.log.AdjustLog, 'log', autospec=True)
    @patch.object(app.log.AdjustLog, 'get_logs', autospec=True)
    def test_trigger_when_source_adjust_exception_should_throw(self, get_logs_mock,
                                                               log_mock,
                                                               get_today_adjust_mock,
                                                               adjust_price_mock):
        adjusts = []
        ad_acb = AdjustInfo("ACB", 0.98, "2018-09-14")
        adjusts.append(ad_acb)
        ad_vnd = AdjustInfo("VND", 0.88, "2018-09-14")
        adjusts.append(ad_vnd)
        get_today_adjust_mock.side_effect = RuntimeError('')
        adjust_price_mock.return_value = True
        get_logs_mock.return_value = []

        self.assertRaises(RuntimeError, self.adjust_price_service.adjust_for_today)

    @patch.object(app.stockbook.Api, 'adjust_price', autospec=True)
    @patch.object(app.finfo.PriceAdjustSource, 'get_today_adjust', autospec=True)
    @patch.object(app.log.AdjustLog, 'log', autospec=True)
    @patch.object(app.log.AdjustLog, 'get_logs', autospec=True)
    def test_trigger_when_adjust_price_exception_should_throw(self, get_logs_mock,
                                                               log_mock,
                                                               get_today_adjust_mock,
                                                               adjust_price_mock):
        adjusts = []
        ad_acb = AdjustInfo("ACB", 0.98, "2018-09-14")
        adjusts.append(ad_acb)
        ad_vnd = AdjustInfo("VND", 0.88, "2018-09-14")
        adjusts.append(ad_vnd)
        get_today_adjust_mock.return_value = adjusts
        adjust_price_mock.side_effect = RuntimeError('')
        get_logs_mock.return_value = []

        self.assertRaises(RuntimeError, self.adjust_price_service.adjust_for_today)