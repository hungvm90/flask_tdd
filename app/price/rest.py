import json
from flask import request, jsonify, current_app
from app import not_found
from . import price_blueprint


@price_blueprint.route("/trigger", methods=["GET"])
def get_stock_price(symbol):
    pass


@price_blueprint.route("/", methods=["GET"])
def get_stock_price_by_symbols():
    return jsonify({
        'data': "data"
    })
