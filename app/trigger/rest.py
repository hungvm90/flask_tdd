import os
import json
from flask import jsonify, current_app
from app.stockbook import Api
from . import adjust_price_service
from . import price_blueprint

stockbook_api = Api("")


def write_adjust_log(ad):
    f = open(current_app.config['DATA_FILE'], mode='a')
    f.write(json.dumps(ad.to_json()))
    f.write(os.linesep)
    f.close()


@price_blueprint.route("/trigger", methods=["POST"])
def get_stock_price():
    adjusts = adjust_price_service.adjust_for_today()
    for ad in adjusts:
        stockbook_api.adjust_price(symbol=ad.symbol, ratio=ad.ratio)
        write_adjust_log(ad)
    return jsonify({
        'adjusts': [ad.to_json() for ad in adjusts]
    })


@price_blueprint.route("/", methods=["GET"])
def get_stock_price_by_symbols():
    return jsonify({})
