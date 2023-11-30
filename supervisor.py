from flask_login import UserMixin

from sql import db


class Supervisor(UserMixin, db.Model):
    supervisor_id = db.Column(db.Integer, primary_key=True)
    supervisor_name = db.Column(db.String, unique=True, nullable=False)
    supervisor_cnic = db.Column(db.String, unique=True, nullable=False)
    supervisor_phone_no = db.Column(db.String, unique=True, nullable=False)
    supervisor_address = db.Column(db.String, unique=True, nullable=False)
    supervisor_password = db.Column(db.String, nullable=False)

    def set_password(self, password):
        self.supervisor_password = password

    # def check_password(self, password):
    #     return check_password_hash(self.supervisor_password, password)

    def get_id(self):
        # Prefix the ID to indicate the user type (admin)
        return self.supervisor_id


def authenticate_supervisor(supervisor_id, password):
    supervisor = Supervisor.query.filter_by(supervisor_id=supervisor_id).first()

    # Print admin_id for debugging
    if supervisor and supervisor.supervisor_password == password:
        return supervisor
    return None
