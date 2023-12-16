from flask import render_template, request, redirect

from interview import Interview
from job_application import Job_application
from sql import db


class Call_interviewDate:
    def interviewdate(self, id):
        # getting applicants filter by id
        obj = Job_application()
        requests = obj.query.filter_by(applicant_id=id).first()
        if request.method == 'POST':
            # storing values in temporary variables
            _id = requests.applicant_id
            date = request.form.get('date')
            time = request.form.get('time')
            remarks = request.form.get('remarks')

            # inserting data into database class model
            entry = Interview(applicant_id=_id, date=date, time=time, remarks=remarks)

            # adding values to database
            db.session.add(entry)
            db.session.commit()

            return redirect("/admincalled")

        return render_template("setinterviewdate.html", id=id)
