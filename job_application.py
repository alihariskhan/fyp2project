from flask import request, render_template, Response
from sql import db
from datetime import datetime


class Job_application(db.Model):
    applicant_id = db.Column(db.Integer, primary_key=True)
    candidate_name = db.Column(db.String, nullable=False)
    candidate_cnic = db.Column(db.String, nullable=False)
    candidate_phone_no = db.Column(db.String, nullable=False)
    candidate_email = db.Column(db.String, nullable=False)
    date = db.Column(db.String, nullable=False)
    candidate_experience = db.Column(db.String, nullable=False)

    def Call_job_apply(self):
        if request.method == 'POST':
            # getting data from data fields
            name = request.form.get('candidate_name')
            nic = request.form.get('candidate_cnic')
            phone = request.form.get('candidate_phone_no')
            email = request.form.get('candidate_email')
            candidate_experience = request.form.get('candidate_experience')

            # inserting data in table class model
            entry = Job_application(candidate_name=name, candidate_cnic=nic, candidate_phone_no=phone,
                                    candidate_email=email, candidate_experience=candidate_experience, date=datetime.now())
            # adding data to database
            db.session.add(entry)
            db.session.commit()

            # Use Response to send a custom response
            return Response("Application submitted successfully!", status=200, content_type='text/plain')
        else:
            return render_template("jobapply.html")
