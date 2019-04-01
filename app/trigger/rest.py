from flask import jsonify, current_app
from . import adjust_price_service
from . import price_blueprint


@price_blueprint.route("/trigger", methods=["POST"])
def get_stock_price():
    adjusts = adjust_price_service.adjust_for_today()
    current_app.sentry.capture_message("adjust price OK")
    return jsonify({
        'adjusts': [ad.to_json() for ad in adjusts]
    })
