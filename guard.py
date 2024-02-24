from sql import db

class Guard(db.Model):
    guard_id = db.Column(db.Integer, primary_key=True)
    guard_name = db.Column(db.String, nullable=False)
    guard_cnic = db.Column(db.String, nullable=False)
    guard_phone = db.Column(db.String, nullable=False)
    guard_email = db.Column(db.String, nullable=False)
    date = db.Column(db.String, nullable=False)
    experience = db.Column(db.String, nullable=False)
    password = db.Column(db.String)
    cost = db.Column(db.Double)





