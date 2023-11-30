from sql import db


class Guard_reservation(db.Model):
    __tablename__ = 'guard_reservation'
    reservation_id = db.Column(db.Integer, primary_key=True, nullable=False)
    res_datetime = db.Column(db.DateTime, nullable=False)
    start_date = db.Column(db.Date, nullable=True)
    end_date = db.Column(db.Date, nullable=True)
    schedule_details = db.Column(db.String, nullable=True)
