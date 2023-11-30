from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from sql import db


class Client(UserMixin, db.Model):
    client_id = db.Column(db.Integer, primary_key=True)
    client_name = db.Column(db.String, unique=True, nullable=False)
    client_cnic = db.Column(db.String, unique=True, nullable=False)
    client_phone_no = db.Column(db.String, unique=True, nullable=False)
    client_address = db.Column(db.String, unique=True, nullable=False)
    password_hash = db.Column(db.String, nullable=False)

    def set_password(self, password):
        self.password_hash = password

    # def check_password(self, password):
    #     return check_password_hash(self.password_hash, password)

    def get_id(self):
        # Prefix the ID to indicate the user type (admin)
        return self.client_id


def authenticate_client(client_id, password):
    client = Client.query.filter_by(client_id=client_id).first()
    if client and client.password_hash == password:
        return client
    return None
