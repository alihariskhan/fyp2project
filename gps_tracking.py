from sql import db


class Gps_Tracking(db.Model):
    __tablename__ = "gps_tracking"
    id = db.Column(db.Integer, primary_key=True)
    guard_id = db.Column(db.Integer, db.ForeignKey("guard.guard_id"), nullable=False)
    latitude = db.Column(db.Double)
    longitude = db.Column(db.Double)
    start_lat = db.Column(db.Double)
    start_long = db.Column(db.Double)
    start_time = db.Column(db.DateTime)
    stop_time = db.Column(db.DateTime)

