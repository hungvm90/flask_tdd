import unittest
import json
import os
from unittest.mock import patch, Mock
import app
from app import create_app
from app.fuck import Simple


class APITestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()

    def tearDown(self):
        self.app_context.pop()

    def delete_data_folder(self):
        if os.path.exists(self.app.config.DATA_FILE):
            os.remove(self.app.config.DATA_FILE)

    @patch.object(app.price.PriceAdjustSource, 'get_today_adjust', autospec=True, return_value=['xxxx'])
    def test_trigger_when_data_file_is_not_exist(self, get_today_adjust_mock):
        x = Simple()
        print(x)
        print(x.f())
        # self.delete_data_folder()
        # response = self.client.post(
        #     '/api/adjust/trigger',
        #     headers={})
        # self.assertEqual(response.status_code, 200)
        # json_response = json.loads(response.get_data(as_text=True))
        # self.assertEqual(json_response['error'], 'not found')

    @patch('app.price.PriceAdjustSource')
    def test_trigger_when_data_file_is_not_exist_x(self, MockClass):
        instance = MockClass.return_value
        instance.get_today_adjust.return_value = ['a', 'b']
        x = Simple()
        print(x)
        print(x.f())
        # self.delete_data_folder()
        # response = self.client.post(
        #     '/api/adjust/trigger',
        #     headers={})
        # self.assertEqual(response.status_code, 200)
        # json_response = json.loads(response.get_data(as_text=True))
        # self.assertEqual(json_response['error'], 'not found')
