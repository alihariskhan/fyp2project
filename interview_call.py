from datetime import datetime

from flask import redirect

from callforinterview import CallForInterview
from job_application import Job_application
from sql import db


class Interview_call:
    def call(self, id):
        # getting applicants filter by id
        requests = Job_application.query.filter_by(applicant_id=id).first()

        # storing values in temporary variables
        _id = requests.applicant_id
        name = requests.candidate_name
        nic = requests.candidate_cnic
        phone = requests.candidate_phone_no
        email = requests.candidate_email
        date = datetime.now()
        experience = requests.candidate_experience

        # inserting data into database class model
        entry = CallForInterview(interviewer_id=_id, interviewer_name=name, interviewer_cnic=nic, interviewer_phone_no=phone,
                          interviewer_email=email, date=date, experience=experience)

        # adding values to database
        db.session.add(entry)
        db.session.commit()
        # deleting applications of applicants (sent for interview)
        deletereq = Job_application.query.filter_by(applicant_id=id).first()
        db.session.delete(deletereq)
        db.session.commit()

        return redirect('/jobrequests')
