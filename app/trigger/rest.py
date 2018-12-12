from flask import jsonify, current_app
from . import adjust_price_service
from . import price_blueprint


@price_blueprint.route("/trigger", methods=["POST"])
def get_stock_price():
    try:
        adjusts = adjust_price_service.adjust_for_today()
        return jsonify({
            'adjusts': [ad.to_json() for ad in adjusts]
        })
    except Exception as e:
        current_app.teams.text("Have some problem when adjust price, please check")
        raise e
