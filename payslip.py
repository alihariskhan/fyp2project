from flask import request, jsonify
from flask_login import current_user
from sqlalchemy import func

from guard import Guard
from guard_attendance import GuardAttendance
from salary_details import Fine_Details
from datetime import datetime


class Payslip:
    def payslip(self):
        absent_count = 0
        late_count = 0
        if request.is_json:
            selected_month = request.json.get('month')
            format_datetime = datetime.strptime(selected_month, "%Y-%m")
            month = format_datetime.month
            year = format_datetime.year

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

            # print(absent_count, late_count)

            fine_details = Fine_Details.query.filter_by(id=1).first()
            guard = Guard.query.filter_by(guard_id=current_user.guard_id).first()
            print(fine_details.late_fine)
            print(fine_details.absent_fine)

            return jsonify({'result': 'Success'})
        else:
            return jsonify({'error': 'Invalid content type, expecting JSON'}), 400
