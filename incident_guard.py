from sql import db


class Incident_Guard(db.Model):
    __tablename__ = "incident_guard"
    id = db.Column(db.Integer, primary_key=True)
    incident_id = db.Column(db.Integer, db.ForeignKey('incident_report.incident_id'), nullable=False)
    guard_id = db.Column(db.Integer, db.ForeignKey('guard.guard_id'), nullable=False)