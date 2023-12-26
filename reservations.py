from datetime import datetime, timedelta
from flask import render_template, redirect
from flask_login import current_user

from guard import Guard
from location_details import location_Details
from client import Client
from client_guard_reservation import Client_Guard_Reservation, Client_Guard_Reservation_History
from guard_reservation import Guard_reservation, Guard_reservation_history
from sql import db


class Reservations:

    def reservations(self):
        reservations = (
            db.session.query(Client_Guard_Reservation, Guard_reservation, Client, location_Details, Guard)
            .select_from(Client_Guard_Reservation)
            .join(Guard_reservation, Client_Guard_Reservation.reservation_id == Guard_reservation.reservation_id)
            .join(Client, Client_Guard_Reservation.client_id == Client.client_id)
            .join(location_Details, location_Details.location_id == Client_Guard_Reservation.location_id)
            .join(Guard, Client_Guard_Reservation.guard_id == Guard.guard_id)
            .filter(Guard_reservation.payment == False)
        )
        return render_template("reservations.html", reservations=reservations)

    def reservation_end(self):
        reservations = (
            db.session.query(Client_Guard_Reservation, Guard_reservation)
            .select_from(Client_Guard_Reservation)
            .join(Guard_reservation, Client_Guard_Reservation.reservation_id == Guard_reservation.reservation_id)
            .filter(Guard_reservation.end_date >= datetime.now().date() - timedelta(days=1))
        )

        if reservations:
            try:
                processed_reservation_ids = set()

                for client_guard_reservation, guard_reservation in reservations:
                    # Check if the reservation_id has already been processed
                    if guard_reservation.reservation_id in processed_reservation_ids:
                        continue

                    # Create and add historical records for Guard_reservation
                    entry_history = Guard_reservation_history(
                        reservation_id=guard_reservation.reservation_id,
                        res_datetime=guard_reservation.res_datetime,
                        start_date=guard_reservation.start_date,
                        end_date=guard_reservation.end_date,
                        schedule_details=guard_reservation.schedule_details,
                        payment=guard_reservation.payment,
                        reservation_end=True,
                        cancel_reservation=False,
                        payment_cancel=False
                    )

                    db.session.add(entry_history)

                    # Mark the reservation_id as processed
                    processed_reservation_ids.add(guard_reservation.reservation_id)

                db.session.commit()

                for client_guard_reservation1, guard_reservation1 in reservations:
                    # Create and add historical records for Client_Guard_Reservation
                    entry_history2 = Client_Guard_Reservation_History(
                        id=client_guard_reservation1.id,
                        client_id=client_guard_reservation1.client_id,
                        reservation_id=client_guard_reservation1.reservation_id,
                        guard_id=client_guard_reservation1.guard_id,
                        location_id=client_guard_reservation1.location_id,
                        duty_shift=client_guard_reservation1.duty_shift,
                        start_time=client_guard_reservation1.start_time,
                        end_time=client_guard_reservation1.end_time
                    )

                    db.session.add(entry_history2)

                db.session.commit()

                # Delete the records from the original tables
                for client_guard_reservation, guard_reservation in reservations:
                    db.session.delete(client_guard_reservation)
                    db.session.delete(guard_reservation)

                db.session.commit()

            except Exception as e:
                print(f"Error processing reservations: {e}")
                # Rollback changes in case of an error
                db.session.rollback()

    def cancel_reservation(self, _id):
        reservations = (
            db.session.query(Client_Guard_Reservation, Guard_reservation)
            .select_from(Client_Guard_Reservation)
            .join(Guard_reservation, Client_Guard_Reservation.reservation_id == Guard_reservation.reservation_id)
            .filter(Guard_reservation.reservation_id == _id).all()
        )

        if reservations:
            try:
                processed_reservation_ids = set()

                for client_guard_reservation, guard_reservation in reservations:
                    # Check if the reservation_id has already been processed
                    if guard_reservation.reservation_id in processed_reservation_ids:
                        continue

                    # Create and add historical records for Guard_reservation
                    entry_history = Guard_reservation_history(
                        reservation_id=guard_reservation.reservation_id,
                        res_datetime=guard_reservation.res_datetime,
                        start_date=guard_reservation.start_date,
                        end_date=guard_reservation.end_date,
                        schedule_details=guard_reservation.schedule_details,
                        payment=guard_reservation.payment,
                        reservation_end=False,
                        cancel_reservation=True,
                        payment_cancel=False
                    )

                    db.session.add(entry_history)

                    # Mark the reservation_id as processed
                    processed_reservation_ids.add(guard_reservation.reservation_id)

                db.session.commit()

                for client_guard_reservation1, guard_reservation1 in reservations:
                    # Create and add historical records for Client_Guard_Reservation
                    entry_history2 = Client_Guard_Reservation_History(
                        id=client_guard_reservation1.id,
                        client_id=client_guard_reservation1.client_id,
                        reservation_id=client_guard_reservation1.reservation_id,
                        guard_id=client_guard_reservation1.guard_id,
                        location_id=client_guard_reservation1.location_id,
                        duty_shift=client_guard_reservation1.duty_shift,
                        start_time=client_guard_reservation1.start_time,
                        end_time=client_guard_reservation1.end_time
                    )

                    db.session.add(entry_history2)

                db.session.commit()

                # Delete the records from the original tables
                for client_guard_reservation, guard_reservation in reservations:
                    db.session.delete(client_guard_reservation)
                    db.session.delete(guard_reservation)

                db.session.commit()

            except Exception as e:
                print(f"Error processing reservations: {e}")
                # Rollback changes in case of an error
                db.session.rollback()

    def payment_cancel(self):
        reservations = (
            db.session.query(Client_Guard_Reservation, Guard_reservation)
            .select_from(Client_Guard_Reservation)
            .join(Guard_reservation, Client_Guard_Reservation.reservation_id == Guard_reservation.reservation_id)
            .filter(Guard_reservation.res_datetime == datetime.now().date() - timedelta(days=3))
            .filter(Guard_reservation.payment == False)
        )

        if reservations:
            try:
                processed_reservation_ids = set()

                for client_guard_reservation, guard_reservation in reservations:
                    # Check if the reservation_id has already been processed
                    if guard_reservation.reservation_id in processed_reservation_ids:
                        continue

                    # Create and add historical records for Guard_reservation
                    entry_history = Guard_reservation_history(
                        reservation_id=guard_reservation.reservation_id,
                        res_datetime=guard_reservation.res_datetime,
                        start_date=guard_reservation.start_date,
                        end_date=guard_reservation.end_date,
                        schedule_details=guard_reservation.schedule_details,
                        payment=guard_reservation.payment,
                        reservation_end=False,
                        cancel_reservation=True,
                        payment_cancel=True  # Updated this to indicate payment cancellation
                    )

                    db.session.add(entry_history)

                    # Mark the reservation_id as processed
                    processed_reservation_ids.add(guard_reservation.reservation_id)

                db.session.commit()

                for client_guard_reservation1, guard_reservation1 in reservations:
                    # Create and add historical records for Client_Guard_Reservation
                    entry_history2 = Client_Guard_Reservation_History(
                        id=client_guard_reservation1.id,
                        client_id=client_guard_reservation1.client_id,
                        reservation_id=client_guard_reservation1.reservation_id,
                        guard_id=client_guard_reservation1.guard_id,
                        location_id=client_guard_reservation1.location_id,
                        duty_shift=client_guard_reservation1.duty_shift,
                        start_time=client_guard_reservation1.start_time,
                        end_time=client_guard_reservation1.end_time
                    )

                    db.session.add(entry_history2)

                db.session.commit()

                # Delete the records from the original tables
                for client_guard_reservation, guard_reservation in reservations:
                    db.session.delete(client_guard_reservation)
                    db.session.delete(guard_reservation)

                db.session.commit()

            except Exception as e:
                print(f"Error processing reservations: {e}")
                # Rollback changes in case of an error
                db.session.rollback()

    def show_reservation_details(self, _id):
        reservations = (
            db.session.query(Client_Guard_Reservation, Guard_reservation, Client, location_Details, Guard)
            .select_from(Client_Guard_Reservation)
            .join(Guard_reservation, Client_Guard_Reservation.reservation_id == Guard_reservation.reservation_id)
            .join(Client, Client_Guard_Reservation.client_id == Client.client_id)
            .join(location_Details, location_Details.location_id == Client_Guard_Reservation.location_id)
            .join(Guard, Client_Guard_Reservation.guard_id == Guard.guard_id)
            .group_by(Client_Guard_Reservation.reservation_id)
            .filter(Guard_reservation.reservation_id == _id)
        )
        guards = (
            db.session.query(Client_Guard_Reservation, Guard_reservation, Client, location_Details, Guard)
            .select_from(Client_Guard_Reservation)
            .join(Guard_reservation, Client_Guard_Reservation.reservation_id == Guard_reservation.reservation_id)
            .join(Client, Client_Guard_Reservation.client_id == Client.client_id)
            .join(location_Details, location_Details.location_id == Client_Guard_Reservation.location_id)
            .join(Guard, Client_Guard_Reservation.guard_id == Guard.guard_id)
            .filter(Guard_reservation.reservation_id == _id)
            .order_by(Guard.guard_id.asc())
        )
        count = guards.count()

        return render_template("show_reservation_details.html", reservations=reservations, guards=guards, count=count)

    def guard_cancel(self, _id):
        guard_cancel = (
            db.session.query(Client_Guard_Reservation, Guard_reservation, Client, location_Details, Guard)
            .select_from(Client_Guard_Reservation)
            .join(Guard_reservation, Client_Guard_Reservation.reservation_id == Guard_reservation.reservation_id)
            .join(Client, Client_Guard_Reservation.client_id == Client.client_id)
            .join(location_Details, location_Details.location_id == Client_Guard_Reservation.location_id)
            .join(Guard, Client_Guard_Reservation.guard_id == Guard.guard_id)
            .filter(Client.client_id == current_user.client_id)
            .filter(Guard.guard_id == _id)
        )

        if guard_cancel:
            guard_delete = (Client_Guard_Reservation.query.filter(Client_Guard_Reservation.guard_id == _id)
                            .filter(Client_Guard_Reservation.client_id == current_user.client_id).first()
                            )
            db.session.delete(guard_delete)
            db.session.commit()

        return redirect("/guard_cancel_page")
