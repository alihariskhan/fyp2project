from flask import flash, redirect
from flask_login import current_user

from guard import Guard
from sql import db


class Client_Guard_Reservation_History(db.Model):
    __tablename__ = 'client_guard_reservation_history'
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.client_id'))
    guard_id = db.Column(db.Integer, db.ForeignKey('guard.guard_id'))
    reservation_id = db.Column(db.Integer, db.ForeignKey('guard_reservation.reservation_id'))
    location_id = db.Column(db.Integer, db.ForeignKey('location_details.location_id'))
    duty_shift = db.Column(db.String, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)


class Client_Guard_Reservation(db.Model):
    __tablename__ = 'client_guard_reservation'
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.client_id'))
    guard_id = db.Column(db.Integer, db.ForeignKey('guard.guard_id'))
    reservation_id = db.Column(db.Integer, db.ForeignKey('guard_reservation.reservation_id'))
    location_id = db.Column(db.Integer, db.ForeignKey('location_details.location_id'))
    duty_shift = db.Column(db.String, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)

    def guard_select(self, _id):
        try:
            # Check if a record with the specified guard_id already exists in Guard_Select
            existing_entry = (Client_Guard_Reservation.query.filter_by(guard_id=_id)
                              .first())

            if existing_entry:
                # If the entry already exists, show an error message
                flash("Guard has already been selected.")
            else:
                # If the entry doesn't exist, proceed with adding a new entry
                guard = Guard.query.get(_id)

                if guard:

                    entry = Client_Guard_Reservation(client_id=current_user.client_id,
                                                     guard_id=_id)

                    db.session.add(entry)
                    db.session.commit()
                    flash("Guard selected successfully.")
                else:
                    flash("Guard not found.")
        except Exception as e:
            # Rollback the transaction in case of an error
            db.session.rollback()
            flash("Error occurred. Please try again.")
            # Log the error for debugging purposes if needed
            print(f"Error: {str(e)}")

        return redirect("/guard_reservation")
