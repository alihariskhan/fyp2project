from datetime import datetime

from flask import render_template
from flask_login import current_user
from sqlalchemy import func

from client_guard_reservation import Client_Guard_Reservation
from guard_reservation import Guard_reservation
from sql import db

from client import Client


class Invoice:
    def invoice(self):
        client = Client.query.filter(Client.client_id == current_user.client_id).first()
        date = datetime.now().date()

        reservation_details = (
            db.session.query(
                Guard_reservation.reservation_id,
                func.count(Client_Guard_Reservation.guard_id).label('guard_count')
            )
            .join(Client_Guard_Reservation,
                  Guard_reservation.reservation_id == Client_Guard_Reservation.reservation_id)
            .filter(Client_Guard_Reservation.client_id == current_user.client_id)
            .group_by(Guard_reservation.reservation_id)
            .all()
        )
        print(f"{reservation_details}")
        return render_template("invoice.html", client=client, date=date, reserv=reservation_details)
