from flask import request, jsonify, redirect
from flask_login import current_user
from sqlalchemy import func

from client_guard_reservation import Client_Guard_Reservation
from guard import Guard
from guard_attendance import GuardAttendance
from guard_reservation import Guard_reservation
from salary_details import Fine_Details
from datetime import datetime
from salary_details import Salary_details
from sql import db


class Payslip:
    def payslip(self):
        absent_count = 0
        late_count = 0

        if request.is_json:
            selected_month = request.json.get('month')
            format_datetime = datetime.strptime(selected_month, "%Y-%m")
            month = format_datetime.month
            year = format_datetime.year

            guard_exist = (Salary_details.query.filter(Salary_details.guard_id == current_user.guard_id)
                           .first())
            if guard_exist:
                ded = guard_exist.deducted_amount
                month_year = guard_exist.month_year
                if ded and month_year:
                    details = Salary_details.query.filter_by(guard_id=current_user.guard_id).first()
                    return jsonify(details)
                else:
                    # Query to get records grouped by month and year
                    results = (
                        GuardAttendance.query
                        .filter_by(guard_id=current_user.guard_id)
                        .filter(func.extract('year', GuardAttendance.datetime) == year)
                        .filter(func.extract('month', GuardAttendance.datetime) == month)
                        .group_by(GuardAttendance.guard_id)
                        .all()
                    )

                    # Print the results
                    for result in results:
                        absent_count = result.query.filter_by(absent=1).count()
                        late_count = result.query.filter_by(late=1).count()

                    print(absent_count, late_count)

                    fine_details = Fine_Details.query.filter_by(id=1).first()
                    print(fine_details.late_fine)
                    print(fine_details.absent_fine)
                    late = fine_details.late_fine
                    absent = fine_details.absent_fine

                    salary_account = Salary_details.query.filter_by(guard_id=current_user.guard_id).first()

                    absent_entry = absent_count * absent
                    late_entry = late_count * late
                    total = absent_entry + late_entry

                    salary_account.deducted_amount = total
                    salary_account.month_year = selected_month
                    db.session.commit()

                    details = Salary_details.query.filter_by(guard_id=current_user.guard_id).first()
                    return jsonify(details)
            else:
                return "not found"
        else:
            return jsonify({'error': 'Invalid content type, expecting JSON'}), 400

