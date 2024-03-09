from sql import db


class Fine_Details(db.Model):
    __tablename__ = 'fine_details'
    id = db.Column(db.Integer, primary_key=True)
    absent_fine = db.Column(db.Double, nullable=False)
    late_fine = db.Column(db.Double, nullable=False)

class Salary_details(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    guard_id = db.Column(db.Integer, db.ForeignKey('guard.guard_id'))
    salary_generated = db.Column(db.Double, nullable=False)
    hours_worked = db.Column(db.Double, nullable=False)
    deducted_amount = db.Column(db.Double)
    month_year = db.Column(db.Date)
