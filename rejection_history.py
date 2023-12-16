from datetime import datetime

from MySQLdb._exceptions import IntegrityError
from flask import request, redirect

from interview import Interview_History
from job_application import Job_application_History
from sql import db


class Rejection_History:


    def truncate(self):
        # Check if it's the 1st date of the month
        today = datetime.now().date()
        first_day_of_month = today.replace(day=1)

        if today == first_day_of_month:
            try:
                # Truncate the tables
                db.session.query(Job_application_History).delete()
                db.session.query(Interview_History).delete()
                db.session.commit()
            except IntegrityError:
                # Handle any exceptions that may occur during the truncation
                db.session.rollback()

    def clear_history(self):

        if request.path == "/clear_history":
            try:
                # Truncate the tables
                db.session.query(Job_application_History).delete()
                db.session.query(Interview_History).delete()
                db.session.commit()
                return redirect("/rejection_history")
            except IntegrityError:
                # Handle any exceptions that may occur during the truncation
                db.session.rollback()
