from flask import Flask, jsonify, current_app
from flask.logging import default_handler
from flask_cors import CORS
import logging
from logging import handlers
from config import config
from .util import make_log_dir
from . import finfo
from . import stockbook
from . import log
from .adjust_price import AdjustPriceService


cors = CORS()
adjust_price_service = AdjustPriceService()


def init_logger(app, config_obj):
    make_log_dir(config_obj.LOG_FOLDER)
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(pathname)s:%(lineno)d %(message)s')
    default_handler.setFormatter(formatter)

    file_handler = handlers.WatchedFileHandler(
        '{}/adjustPriceForRecommendation.log'.format(config_obj.LOG_FOLDER)
    )
    file_handler.setLevel(logging.WARN)
    file_handler.setFormatter(formatter)
    app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.DEBUG if app.debug else logging.WARN)
    app.logger.info("App log folder: {}".format(config_obj.LOG_FOLDER))
    adjust_price_service.init(app)

    @app.route("/")
    def info():
        return jsonify({'status': "OK", "version": current_app.config['APP_VERSION']})

    @app.route("/health")
    def health():
        return jsonify({'status': 'OK', 'data': {}})


def create_app(config_name):
    config_obj = config[config_name]
    app = Flask(__name__)
    app.url_map.strict_slashes = False
    app.config.from_object(config_obj)
    init_logger(app, config_obj)
    config_obj.init_app(app)
    setup_default_app_error_handler(app)
    cors.init_app(app)

    from .trigger import price_blueprint
    app.register_blueprint(price_blueprint, url_prefix='/api/adjust')
    app.logger.info("start app with {}".format(config_obj.PRICE_ADJUST_SOURCE_URL))
    app.logger.info("start app with {}".format(config_obj.STOCKBOOK_API))
    app.logger.info("start app with {}".format(config_obj.DATA_FILE))
    return app


def bad_request(message, code):
    response = jsonify({'error': code, 'message': message})
    response.status_code = 400
    return response


def unauthorized(message, code):
    response = jsonify({'error': code, 'message': message})
    response.status_code = 401
    return response


def forbidden(message, code):
    response = jsonify({'error': code, 'message': message})
    response.status_code = 403
    return response


def not_found(message, code):
    response = jsonify({'error': code, 'message': message})
    response.status_code = 404
    return response


def internal_error(message, code):
    response = jsonify({'error': code, 'message': message})
    response.status_code = 500
    return response


def setup_default_app_error_handler(app):

    @app.errorhandler(Exception)
    def error_handle(error):
        app.logger.error(str(error))
        app.logger.exception(error)
        return internal_error(str(error), 500)

    @app.errorhandler(404)
    def page_not_found(e):
        return not_found('not found', 404)

