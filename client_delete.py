from flask import redirect, request

from client_guard_reservation import Client_Guard_Reservation
from sql import db


class Client_delete:
    def delete(self, guard_id):
        if request.method == 'GET':

            guard_select_delete = Client_Guard_Reservation.query.filter_by(guard_id=guard_id).first()

            if guard_select_delete:
                db.session.delete(guard_select_delete)
                db.session.commit()
                return redirect('/reservation_details')

            else:
                # Handle the case where a guard or a guard_select request was found
                return "No match found"
