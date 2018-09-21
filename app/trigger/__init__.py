
from flask import Blueprint
from app import adjust_price_service
price_blueprint = Blueprint('trigger', __name__)

from . import rest
