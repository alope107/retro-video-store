from flask import Blueprint, jsonify, request, abort, make_response

from app import db
from app.models.customer import Customer
from app.models.video import Video

customers_bp = Blueprint("customers", __name__, url_prefix="/customers")
CUSTOMER_PARAMS = ("name", "postal_code", "phone")

def validate_params_or_abort(body, params):
    for attr in params:
        if attr not in body:
            abort(make_response({"details": f"Request body must include {attr}."}, 400))

@customers_bp.route("", methods=["GET"])
def get_all_customers():
    return jsonify([c.to_dict() for c in Customer.query])

@customers_bp.route("", methods=["POST"])
def create_customers():
    body = request.get_json()

    validate_params_or_abort(body, CUSTOMER_PARAMS)

    customer = Customer(name=body["name"], 
                        postal_code=body["postal_code"],
                        phone=body["phone"])

    db.session.add(customer)
    db.session.commit()

    return customer.to_dict(), 201

@customers_bp.route("/<customer_id>", methods=["GET", "DELETE", "PUT"])
def handle_one_customer(customer_id):
    try:
        customer_id = int(customer_id)
    except ValueError:
        return f"Invalid customer id '{customer_id}'",400

    customer = Customer.query.get(customer_id)
    if customer is None:
        return {"message": f"Customer {customer_id} was not found"}, 404

    if request.method == "GET":
        return customer.to_dict()
    elif request.method == "DELETE":
        db.session.delete(customer)
        db.session.commit()

        return {"id": customer.id}
    elif request.method == "PUT":
        body = request.get_json()
        validate_params_or_abort(body, CUSTOMER_PARAMS)

        customer.name = body["name"]
        customer.postal_code = body["postal_code"]
        customer.phone = body["phone"]

        db.session.commit()
        return customer.to_dict()


videos_bp = Blueprint("videos", __name__, url_prefix="/videos")
VIDEO_PARAMS = ("title", "release_date", "total_inventory")

@videos_bp.route("", methods=["GET"])
def get_all_videos():
    return jsonify([c.to_dict() for c in Video.query])

@videos_bp.route("", methods=["POST"])
def create_videos():
    body = request.get_json()

    validate_params_or_abort(body, VIDEO_PARAMS)

    video = Video(title=body["title"], 
                  release_date=body["release_date"],
                  total_inventory=body["total_inventory"])

    db.session.add(video)
    db.session.commit()

    return video.to_dict(), 201

@videos_bp.route("/<video_id>", methods=["GET", "DELETE", "PUT"])
def handle_one_video(video_id):
    try:
        video_id = int(video_id)
    except ValueError:
        return f"Invalid video id '{video_id}'",400

    video = Video.query.get(video_id)
    if video is None:
        return {"message": f"Video {video_id} was not found"}, 404

    if request.method == "GET":
        return video.to_dict()
    elif request.method == "DELETE":
        db.session.delete(video)
        db.session.commit()

        return {"id": video.id}
    elif request.method == "PUT":
        body = request.get_json()
        validate_params_or_abort(body, VIDEO_PARAMS)

        video.title = body["title"]
        video.release_date = body["release_date"]
        video.total_inventory = body["total_inventory"]

        db.session.commit()
        return video.to_dict()