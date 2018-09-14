import os


def make_log_dir(path):
    try:
        os.mkdir(path)
    except:
        pass