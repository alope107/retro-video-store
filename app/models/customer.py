from app import db

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    postal_code = db.Column(db.String)
    phone_number = db.Column(db.String)
    registered_at = db.Column(db.DateTime)