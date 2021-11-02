from app import db

def default_available(context):
    return context.get_current_parameters()['total_inventory']

class Video(db.Model):
    __tablename__ = "video"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    release_date = db.Column(db.Date)
    total_inventory = db.Column(db.Integer)
    available_inventory = db.Column(db.Integer, default=default_available)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "release_date": str(self.release_date),
            "total_inventory": self.total_inventory,
            "available_inventory": self.available_inventory
        }