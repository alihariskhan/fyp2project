from sql import db


class location_Details(db.Model):
    __tablename__ = 'location_details'
    location_id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String, nullable=False)
