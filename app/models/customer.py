from app import db

class Customer(db.Model):
    __tablename__ = "customer"

    name = db.Column(db.String)
    postal_code = db.Column(db.String)
    phone = db.Column(db.String)
    videos_checked_out_count = db.Column(db.Integer, default=0)
    registered_at = db.Column(db.DateTime)
    id = db.Column(db.Integer, primary_key=True)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "postal_code": self.postal_code,
            "phone": self.phone,
            "registered_at": str(self.registered_at),
            "videos_checked_out_count": self.videos_checked_out_count,
        }
