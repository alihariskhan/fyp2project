from sql import db


class CallForInterview(db.Model):
    __tablename__ = 'callforinterview'
    interviewer_id = db.Column(db.Integer, primary_key=True)
    interviewer_name = db.Column(db.String, nullable=False)
    interviewer_cnic = db.Column(db.String, nullable=False)
    interviewer_phone_no = db.Column(db.String, nullable=False)
    interviewer_email = db.Column(db.String, nullable=False)
    date = db.Column(db.String, nullable=False)
    experience = db.Column(db.String, nullable=False)
