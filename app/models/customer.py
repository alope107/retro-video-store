from app import db

class Customer(db.Model):
    postal_code = db.Column(db.String)
    phone_number = db.Column(db.String)
    registered_at = db.Column(db.DateTime)
    id = db.Column(db.Integer, primary_key=True)

    def to_dict(self):
        return {
            "id": self.id,
            "postal_code": self.postal_code,
            "phone_number": self.phone_number,
            "registered_at": str(self.registered_at)
        }
