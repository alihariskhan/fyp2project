from flask import render_template
from flask_login import current_user

from sql import db
from client_guard_reservation import Client_Guard_Reservation
from guard_reservation import Guard_reservation
from guard import Guard
from location_details import location_Details
from client import Client


class Guard_Schedule:
    def guard_schedule(self):
        schedule = (
            db.session.query(Client_Guard_Reservation, Guard_reservation, location_Details, Guard)
            .select_from(Client_Guard_Reservation)
            .join(Guard_reservation, Client_Guard_Reservation.reservation_id == Guard_reservation.reservation_id)
            .join(location_Details, location_Details.location_id == Client_Guard_Reservation.location_id)
            .join(Guard, Client_Guard_Reservation.guard_id == Guard.guard_id)
            .filter(Guard_reservation.payment == True)
        )

        return render_template("guard_schedule.html", schedule=schedule)

    def my_guard_schedule(self):
        schedule = (
            db.session.query(Client_Guard_Reservation, Guard_reservation, Client, location_Details, Guard)
            .select_from(Client_Guard_Reservation)
            .join(Guard_reservation, Client_Guard_Reservation.reservation_id == Guard_reservation.reservation_id)
            .join(Client, Client_Guard_Reservation.client_id == Client.client_id)
            .join(location_Details, location_Details.location_id == Client_Guard_Reservation.location_id)
            .join(Guard, Client_Guard_Reservation.guard_id == Guard.guard_id)
            .filter(Guard_reservation.payment == True)
            .filter(Client.client_id == current_user.client_id)
        )

        return render_template("my_guard_schedule.html", schedule=schedule)
