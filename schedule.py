from flask import request, render_template

from guard import Guard
from location_details import location_Details
from client import Client
from client_guard_reservation import Client_Guard_Reservation
from guard_reservation import Guard_reservation
from sql import db


class Schedule:

    def schedule(self):
        reservations = (db.session.query(Client_Guard_Reservation, Guard_reservation, Client, location_Details, Guard)
                        .select_from(Client_Guard_Reservation)
                        .join(Guard_reservation,
                              Client_Guard_Reservation.reservation_id == Guard_reservation.reservation_id)
                        .join(Client, Client_Guard_Reservation.client_id == Client.client_id)
                        .join(location_Details, location_Details.location_id == Client_Guard_Reservation.location_id)
                        .join(Guard, Client_Guard_Reservation.guard_id == Guard.guard_id)
                        .filter(Guard_reservation.payment == False)
                        )
        return render_template("guard_schedule.html", reservations=reservations)
