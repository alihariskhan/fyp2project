from sql import db


class Guard_reservation(db.Model):
    __tablename__ = 'guard_reservation'
    reservation_id = db.Column(db.Integer, primary_key=True, nullable=False)
    res_datetime = db.Column(db.DateTime, nullable=False)
    start_date = db.Column(db.Date, nullable=True)
    end_date = db.Column(db.Date, nullable=True)
    schedule_details = db.Column(db.String, nullable=True)
    payment = db.Column(db.Boolean, nullable=False, default=False)


class Guard_reservation_history(db.Model):
    __tablename__ = 'guard_reservation_history'
    reservation_id = db.Column(db.Integer, primary_key=True, nullable=False)
    res_datetime = db.Column(db.DateTime, nullable=False)
    start_date = db.Column(db.Date, nullable=True)
    end_date = db.Column(db.Date, nullable=True)
    schedule_details = db.Column(db.String, nullable=True)
    payment = db.Column(db.Boolean, nullable=False, default=False)
    reservation_end = db.Column(db.Boolean, nullable=False, default=False)
    cancel_reservation = db.Column(db.Boolean, nullable=False, default=False)
    payment_cancel = db.Column(db.Boolean, nullable=False, default=False)
