from app import db

class Rental(db.Model):
    id = db.Column(db.Integer, primary_key=True)