class AdjustLog(object):
    def __init__(self, file_path):
        self.file_path = file_path

    def log(self, adjust_price):
        print("log to file " + self.file_path)

    def get_logs(self):
        print("get logs from " + self.file_path)