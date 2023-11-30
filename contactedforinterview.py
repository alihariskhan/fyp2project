from sql import db


class Contactedforinterview(db.Model):
    interviewee_id = db.Column(db.Integer, primary_key=True)
    interviewee_name = db.Column(db.String, nullable=False)
    interviewee_cnic = db.Column(db.String, nullable=False)
    interviewee_phone_no = db.Column(db.String, nullable=False)
    interviewee_email = db.Column(db.String, nullable=False)
    date = db.Column(db.String, nullable=False)
    experience = db.Column(db.String, nullable=False)
    remarks = db.Column(db.String, nullable=False)
