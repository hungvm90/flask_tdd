import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SSL_REDIRECT = False
    LOG_FOLDER = './'
    APP_VERSION = 'dev'
    PRICE_ADJUST_SOURCE_URL = ''
    STOCKBOOK_API = ''
    TOKEN = ''
    DATA_FILE = os.environ.get('DEFAULT') or \
        os.path.join(basedir, 'data_dev.dat')

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    DATA_FILE = os.environ.get('DEFAULT') or \
                os.path.join(basedir, 'data_dev.dat')


class TestingConfig(Config):
    TESTING = True
    APP_VERSION = 'test'
    WTF_CSRF_ENABLED = False
    DATA_FILE = os.environ.get('DEFAULT') or \
                os.path.join(basedir, 'data_test.dat')


class ProductionConfig(Config):
    LOG_FOLDER = os.getenv("LOG_FOLDER") or './'
    APP_VERSION = os.getenv("APP_VERSION") or 'dev'
    PRICE_ADJUST_SOURCE_URL = os.getenv("PRICE_ADJUST_SOURCE_URL")
    STOCKBOOK_API = os.getenv("STOCKBOOK_API")
    TOKEN = os.getenv("TOKEN")
    DATA_FILE = os.getenv("DATA_FILE")

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)


class HerokuConfig(ProductionConfig):
    SSL_REDIRECT = True if os.environ.get('DYNO') else False

    @classmethod
    def init_app(cls, app):
        ProductionConfig.init_app(app)

        # handle reverse proxy server headers
        from werkzeug.contrib.fixers import ProxyFix
        app.wsgi_app = ProxyFix(app.wsgi_app)

        # log to stderr
        import logging
        from logging import StreamHandler
        file_handler = StreamHandler()
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)


class DockerConfig(ProductionConfig):
    @classmethod
    def init_app(cls, app):
        ProductionConfig.init_app(app)

        # log to stderr
        import logging
        from logging import StreamHandler
        file_handler = StreamHandler()
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)


class UnixConfig(ProductionConfig):
    @classmethod
    def init_app(cls, app):
        ProductionConfig.init_app(app)

        # log to syslog
        import logging
        from logging.handlers import SysLogHandler
        syslog_handler = SysLogHandler()
        syslog_handler.setLevel(logging.INFO)
        app.logger.addHandler(syslog_handler)


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'heroku': HerokuConfig,
    'docker': DockerConfig,
    'unix': UnixConfig,

    'default': DevelopmentConfig
}
