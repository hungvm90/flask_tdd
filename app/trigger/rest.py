from flask import jsonify
from . import adjust_price_service
from . import price_blueprint


@price_blueprint.route("/trigger", methods=["POST"])
def get_stock_price():
    adjusts = adjust_price_service.adjust_for_today()
    return jsonify({
        'adjusts': [ad.to_json() for ad in adjusts]
    })
