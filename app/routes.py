from datetime import date, timedelta

from flask import Blueprint, jsonify, request, abort, make_response

from app import db
from app.models.customer import Customer
from app.models.rental import Rental
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
        Rental.query.filter_by(customer_id=customer_id).delete()

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

@customers_bp.route("/<customer_id>/rentals", methods=["GET"])
def get_videos_from_customer(customer_id):
    try:
        customer_id = int(customer_id)
    except ValueError:
        return f"Invalid customer id '{customer_id}'",400

    customer = Customer.query.get(customer_id)
    if customer is None:
        return {"message": f"Customer {customer_id} was not found"}, 404

    videos = db.session.query(Video).join(Rental).filter_by(customer_id=customer_id)
    return jsonify([v.to_dict() for v in videos])


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
        for rental in Rental.query.filter_by(video_id=video_id):
            customer = Customer.query.get(rental.customer_id)
            customer.videos_checked_out_count -= 1
            db.session.delete(rental)

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

@videos_bp.route("/<video_id>/rentals", methods=["GET"])
def get_customers_from_video(video_id):
    try:
        video_id = int(video_id)
    except ValueError:
        return f"Invalid video id '{video_id}'",400

    video = Video.query.get(video_id)
    if video is None:
        return {"message": f"Video {video_id} was not found"}, 404

    customers = db.session.query(Customer).join(Rental).filter_by(video_id=video_id)
    return jsonify([c.to_dict() for c in customers])

rentals_bp = Blueprint("rentals", __name__, url_prefix="/rentals")
RENTAL_PARAMS = ("customer_id", "video_id")

def get_customer_and_video_or_abort(body):
    validate_params_or_abort(body, RENTAL_PARAMS)

    video_id, customer_id = body["video_id"], body["customer_id"]

    try:
        video_id = int(video_id)
    except ValueError:
        abort(make_response(f"Invalid video id '{video_id}'",400))

    video = Video.query.get(video_id)
    if video is None:
        abort(make_response({"message": f"Video {video_id} was not found"}, 404))

    try:
        customer_id = int(customer_id)
    except ValueError:
        abort(make_response(f"Invalid customer id '{customer_id}'",400))

    customer = Customer.query.get(customer_id)
    if customer is None:
        abort(make_response({"message": f"Customer {customer_id} was not found"}, 404))

    return customer, video

    

@rentals_bp.route("check-out", methods=["POST"])
def check_out():
    body = request.get_json()

    customer, video = get_customer_and_video_or_abort(body)
    customer_id, video_id = customer.id, video.id

    if video.available_inventory == 0:
        return {"message": "Could not perform checkout"}, 400

    due_date = date.today() + timedelta(days=7)
    rental = Rental(
        customer_id=customer_id,
        video_id=video_id,
        due_date=due_date
    )

    db.session.add(rental)

    customer.videos_checked_out_count += 1
    video.available_inventory -= 1

    db.session.commit()

    return {
        "customer_id": customer_id,
        "video_id": video_id,
        "videos_checked_out_count": customer.videos_checked_out_count,
        "available_inventory": video.available_inventory
    }

@rentals_bp.route("/check-in", methods=["POST"])
def check_in():
    body = request.get_json()

    customer, video = get_customer_and_video_or_abort(body)
    customer_id, video_id = customer.id, video.id

    rentals = Rental.query.filter_by(customer_id=customer_id).filter_by(video_id=video_id).all()
    if rentals == []:
        return {"message": f"No outstanding rentals for customer # {customer_id} and video {video_id}"}, 400
    
    # If there are multiple copies of the same movie checked out to the same customer, choose one arbitrarily
    rental = rentals[0]

    db.session.delete(rental)

    customer.videos_checked_out_count -= 1
    video.available_inventory += 1

    db.session.commit()

    return {
        "customer_id": customer_id,
        "video_id": video_id,
        "videos_checked_out_count": customer.videos_checked_out_count,
        "available_inventory": video.available_inventory
    }

