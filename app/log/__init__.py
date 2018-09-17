import os
import json
from app.finfo import AdjustInfo

class AdjustLog(object):
    def __init__(self, file_path):
        self.file_path = file_path

    def log(self, adjust_price):
        with open(self.file_path, mode='a') as f:
            f.write(json.dumps(adjust_price.to_json()))
            f.write(os.linesep)

    def get_logs(self):
        if os.path.exists(self.file_path):
            adjusted = []
            with open(self.file_path) as f:
                for line in f:
                    adjusted.append(AdjustInfo.from_json(json.loads(line)))
            return adjusted
        else:
            raise RuntimeError('Log file not exist')