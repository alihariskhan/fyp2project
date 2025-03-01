import uuid
from datetime import datetime

from flask import render_template, redirect
from flask_login import current_user
from sqlalchemy import func

from client_guard_reservation import Client_Guard_Reservation
from guard import Guard
from guard_reservation import Guard_reservation
from sql import db

from client import Client
from salary_details import Salary_details


class Invoice(db.Model):
    invoice_id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.client_id'))
    datetime = db.Column(db.DateTime)
    total_amount = db.Column(db.Double)

    def invoice(self, _id):
        invoice_number = generate_invoice_number()
        total_sum = 0

        reservation_details = (
            db.session.query(
                Guard_reservation.reservation_id,
                Client_Guard_Reservation.hours,
                Guard_reservation.days,
                func.group_concat(Guard.guard_id).label('guard_id'),
                func.group_concat(Guard.guard_name).label('guard_name'),
                func.group_concat(Guard.cost).label('cost'),
                func.count(Client_Guard_Reservation.guard_id).label('guard_count')
            )
            .join(Client_Guard_Reservation,
                  Guard_reservation.reservation_id == Client_Guard_Reservation.reservation_id)
            .join(Guard,
                  Client_Guard_Reservation.guard_id == Guard.guard_id)
            .filter(Client_Guard_Reservation.client_id == _id)
            .filter(Guard_reservation.payment == 0)
            .group_by(Guard.guard_id)
            .all()
        )

        reservations_with_costs = []  # Initialize the list outside the loop

        for reservation in reservation_details:
            # Convert values to numeric types before multiplication
            cost = [float(c) for c in reservation.cost.strip().split(',')]
            hours = float(reservation.hours)
            days = float(reservation.days)
            hours_worked = hours * days
            guard_id = reservation.guard_id

            total_cost = sum(cost * hours * days for cost in cost)

            guard = Guard.query.filter_by(guard_id=reservation.guard_id).first()
            guard_salary = guard.cost*hours_worked

            entry = Salary_details(hours_worked=hours_worked, guard_id=guard_id, salary_generated=guard_salary)
            db.session.add(entry)
            db.session.commit()

            total_sum += total_cost  # Accumulate the total sum

            # Use a dictionary for each reservation
            reservation_with_cost = {
                'reservation_id': reservation.reservation_id,
                'total_cost': total_cost
                # Add any other details you want to include
            }

            reservations_with_costs.append(reservation_with_cost)  # Append to the list

            print(reservations_with_costs)  # Print inside the loop if you want to see each iteration

        invoice_exist = Invoice.query.filter_by(client_id=_id).first()

        if invoice_exist:
            pass

        else:
            entry = Invoice(
                invoice_id=invoice_number,
                client_id=_id,
                datetime=datetime.now(),
                total_amount=total_sum
            )

            # Add and commit the new invoice to the database
            db.session.add(entry)
            db.session.commit()

        invoice_no = Invoice.query.filter_by(client_id=_id).first()

        return redirect('/client_list')

        # return render_template("invoice_generate.html", client=client, date=date, reserv=reservation_details,
        #                        reservations_with_costs=reservations_with_costs, total_sum=total_sum,
        #                        invoice_no=invoice_no)


# Function to generate a simple invoice number
def generate_invoice_number():
    return f"INV{datetime.now().strftime('%Y%m%d%H%M%S')}"
