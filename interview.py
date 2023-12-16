from sql import db


class Interview(db.Model):
    __tablename__ = 'interview'
    interview_id = db.Column(db.Integer, primary_key=True)
    applicant_id = db.Column(db.Integer, db.ForeignKey('job_application.applicant_id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    remarks = db.Column(db.String, nullable=False)


class Interview_History(db.Model):
    __tablename__ = 'interview_history'
    id = db.Column(db.Integer, primary_key=True)
    applicant_id = db.Column(db.Integer, db.ForeignKey('job_application_history.applicant_id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
