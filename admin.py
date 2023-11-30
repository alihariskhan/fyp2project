from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from sql import db


class Admin(UserMixin, db.Model):
    admin_id = db.Column(db.Integer, primary_key=True)
    admin_name = db.Column(db.String, unique=True, nullable=False)
    password_hash = db.Column(db.String, nullable=False)

    def set_password(self, password):
        self.password_hash = password

    # def check_password(self, password):
    #     return check_password_hash(self.password_hash, password)

    def get_id(self):
        # Prefix the ID to indicate the user type (admin)
        return self.admin_id


def authenticate_admin(admin_id, password):
    admin = Admin.query.filter_by(admin_id=admin_id).first()

    # Print admin_id for debugging
    if admin and admin.password_hash == password:
        return admin
    return None
