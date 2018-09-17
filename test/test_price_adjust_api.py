import unittest
import json
from unittest.mock import patch, Mock
from app import create_app
from app.finfo import AdjustInfo


class APITestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()

    def tearDown(self):
        self.app_context.pop()

    @patch('app.trigger.rest.adjust_price_service')
    def test_trigger_when_success_should_return_adjusted(self, mock_adjust_price_service):
        adjusts = []
        ad_acb = AdjustInfo("ACB", 0.98, "2018-09-14")
        adjusts.append(ad_acb)
        ad_vnd = AdjustInfo("VND", 0.88, "2018-09-14")
        adjusts.append(ad_vnd)
        mock_adjust_price_service.adjust_for_today = Mock()
        mock_adjust_price_service.adjust_for_today.return_value = adjusts
        response = self.client.post(
            '/api/adjust/trigger',
            headers={})
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.get_data(as_text=True))
        self.assertIsNotNone(json_response.get('adjusts'))
        self.assertTrue(ad_acb.to_json() in json_response.get('adjusts'))
        self.assertTrue(ad_vnd.to_json() in json_response.get('adjusts'))
        mock_adjust_price_service.adjust_for_today.assert_called_once()

    @patch('app.trigger.rest.adjust_price_service')
    def test_trigger_when_exception_should_return_adjusted(self, mock_adjust_price_service):
        error_msg = "some thing happen"
        mock_adjust_price_service.adjust_for_today = Mock()
        mock_adjust_price_service.adjust_for_today.side_effect = RuntimeError(error_msg)
        response = self.client.post(
            '/api/adjust/trigger',
            headers={})
        self.assertEqual(response.status_code, 500)
        json_response = json.loads(response.get_data(as_text=True))
        self.assertEqual(json_response.get('code'), 500)
        self.assertEqual(json_response.get('message'), error_msg)
        mock_adjust_price_service.adjust_for_today.assert_called_once()
