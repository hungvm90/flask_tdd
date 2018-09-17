import unittest
import os
import json
from app.finfo import AdjustInfo
from app.log import AdjustLog


class AdjustLogTest(unittest.TestCase):
    def setUp(self):
        self._file_path = 'adjust.dat'
        self._log = AdjustLog(self._file_path)

    def tearDown(self):
        pass

    def delete_log(self):
        if os.path.exists(self._file_path):
            os.remove(self._file_path)

    def test_when_file_not_exist_should_create_new(self):
        self.delete_log()
        ad_acb = AdjustInfo("ACB", 0.98, "2018-09-14")
        self._log.log(ad_acb)

        self.assertTrue(os.path.exists(self._file_path))
        f = open(self._file_path)
        lines = f.readlines()
        lines = [line.strip() for line in lines if line]
        self.assertEqual(1, len(lines))
        self.assertEqual(ad_acb, AdjustInfo.from_json(json.loads(lines[0])))

    def test_when_file_exist_should_append(self):
        self.delete_log()
        ad_acb = AdjustInfo("ACB", 0.98, "2018-09-14")
        ad_vnd = AdjustInfo("VND", 0.88, "2018-09-14")
        with open(self._file_path, mode='w') as f:
            f.write(json.dumps(ad_acb.to_json()))
            f.write(os.linesep)
        self._log.log(ad_vnd)

        self.assertTrue(os.path.exists(self._file_path))
        f = open(self._file_path)
        lines = f.readlines()
        lines = [line.strip() for line in lines if line]
        self.assertEqual(2, len(lines))
        self.assertEqual(ad_acb, AdjustInfo.from_json(json.loads(lines[0])))
        self.assertEqual(ad_vnd, AdjustInfo.from_json(json.loads(lines[1])))

    def test_get_logs_when_file_not_exist(self):
        self.delete_log()
        self.assertRaises(RuntimeError, self._log.get_logs)

    def test_get_logs_when_file_empty(self):
        with open(self._file_path, mode='w') as f:
            pass
        adjusted = self._log.get_logs()
        self.assertIsNotNone(adjusted)
        self.assertEqual(0, len(adjusted))

    def test_get_logs_when_file_not_empty(self):
        self.delete_log()
        ad_acb = AdjustInfo("ACB", 0.98, "2018-09-14")
        ad_vnd = AdjustInfo("VND", 0.88, "2018-09-14")
        self._log.log(ad_acb)
        self._log.log(ad_vnd)
        adjusted = self._log.get_logs()
        self.assertIsNotNone(adjusted)
        self.assertEqual(2, len(adjusted))
        self.assertTrue(ad_vnd in adjusted)
        self.assertTrue(ad_acb in adjusted)
