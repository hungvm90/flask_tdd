import unittest
import json
from app import create_app, bad_request, forbidden, not_found, unauthorized, internal_error


class APITestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()

    def tearDown(self):
        self.app_context.pop()

    def test_health_check(self):
        response = self.client.get(
            '/health',
            headers={})
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.get_data(as_text=True))
        self.assertTrue('OK' == json_response.get('status'))
        self.assertTrue({} == json_response.get('data'))

    def test_app_info(self):
        response = self.client.get(
            '/',
            headers={})
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.get_data(as_text=True))
        self.assertTrue('OK' == json_response.get('status'))
        self.assertEqual('test', json_response.get('version'))

    def test_app_info(self):
        response = self.client.get(
            '/not_found',
            headers={})
        self.assertEqual(response.status_code, 404)
        json_response = json.loads(response.get_data(as_text=True))
        self.assertEqual(404, json_response.get('error'))
        self.assertEqual('not found', json_response.get('message'))

    def test_bad_request(self):
        msg = 'test_bad_request'
        code = 1234
        res = bad_request(msg, code)
        self.assertEqual(msg, res.json['message'])
        self.assertEqual(code, res.json['error'])
        self.assertEqual(400, res.status_code)

    def test_forbidden(self):
        msg = 'test_forbidden'
        code = 12345
        res = forbidden(msg, code)
        self.assertEqual(msg, res.json['message'])
        self.assertEqual(code, res.json['error'])
        self.assertEqual(403, res.status_code)

    def test_not_found(self):
        msg = 'test_not_found'
        code = 'âsav'
        res = not_found(msg, code)
        self.assertEqual(msg, res.json['message'])
        self.assertEqual(code, res.json['error'])
        self.assertEqual(404, res.status_code)

    def test_unauthorized(self):
        msg = 'test_unauthorized'
        code = 12345
        res = unauthorized(msg, code)
        self.assertEqual(msg, res.json['message'])
        self.assertEqual(code, res.json['error'])
        self.assertEqual(401, res.status_code)

    def test_internal_error(self):
        msg = 'test_internal_error'
        code = 12345
        res = internal_error(msg, code)
        self.assertEqual(msg, res.json['message'])
        self.assertEqual(code, res.json['error'])
        self.assertEqual(500, res.status_code)
