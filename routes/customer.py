from app import db
from app.models.customer import Customer
from flask import Blueprint, jsonify, make_response, request

customers_bp = Blueprint("customers", __name__, url_prefix="/customers")

@customers_bp.route("", methods=["GET"])
def get_all_customers():
    customers = Customer.query.all()

    