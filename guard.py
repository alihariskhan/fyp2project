from flask_login import UserMixin

from sql import db


class Guard(UserMixin, db.Model):
    guard_id = db.Column(db.Integer, primary_key=True)
    guard_name = db.Column(db.String, nullable=False)
    guard_cnic = db.Column(db.String, nullable=False)
    guard_phone = db.Column(db.String, nullable=False)
    guard_email = db.Column(db.String, nullable=False)
    date = db.Column(db.String, nullable=False)
    experience = db.Column(db.String, nullable=False)
    password = db.Column(db.String)
    cost = db.Column(db.Double)

    def get_id(self):
        # Prefix the ID to indicate the user type (guard)
        return self.guard_id


def authenticate_guard(guard_id, password):
    guard = Guard.query.filter_by(guard_id=guard_id).first()

    # Print guard_id for debugging
    if guard and guard.password == password:
        return guard
    return None
