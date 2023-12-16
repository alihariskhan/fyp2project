from datetime import datetime

from flask import request, render_template, Response

from sql import db


class Job_application_History(db.Model):
    __tablename__ = 'job_application_history'
    applicant_id = db.Column(db.Integer, primary_key=True)
    candidate_name = db.Column(db.String, nullable=False)
    candidate_cnic = db.Column(db.String, nullable=False)
    candidate_phone_no = db.Column(db.String, nullable=False)
    candidate_email = db.Column(db.String, nullable=False)
    date = db.Column(db.String, nullable=False)
    candidate_experience = db.Column(db.String, nullable=False)
    timestamp = db.Column(db.String, nullable=False)
    application_operation = db.Column(db.Boolean, nullable=False)
    interview_operation = db.Column(db.Boolean, nullable=False)


class Job_application(db.Model):
    applicant_id = db.Column(db.Integer, primary_key=True)
    candidate_name = db.Column(db.String, nullable=False)
    candidate_cnic = db.Column(db.String, nullable=False)
    candidate_phone_no = db.Column(db.String, nullable=False)
    candidate_email = db.Column(db.String, nullable=False)
    date = db.Column(db.String, nullable=False)
    candidate_experience = db.Column(db.String, nullable=False)
    interview_request = db.Column(db.Boolean, nullable=False, default=False)

    def Call_job_apply(self):
        if request.method == 'POST':
            # getting data from data fields
            name = request.form.get('candidate_name')
            nic = request.form.get('candidate_cnic')
            phone = request.form.get('candidate_phone_no')
            email = request.form.get('candidate_email')
            candidate_experience = request.form.get('candidate_experience')

            # checking by cnic to stop multiple applications by an applicant
            check = Job_application.query.filter_by(candidate_cnic=nic).first()
            check_in_history = (Job_application_History.query.filter_by(candidate_cnic=nic,
                                                                        application_operation=True,
                                                                        interview_operation=False).first())

            check_in_history2 = (Job_application_History.query.filter_by(candidate_cnic=nic,
                                                                         application_operation=False,
                                                                         interview_operation=True).first())
            if check:
                return Response("Already Submitted!", status=201, content_type='text/plan')
            elif check_in_history:
                return Response("Application Already Rejected!", status=202, content_type='text/plan')
            elif check_in_history2:
                return Response("Already Rejected in Interview!", status=203, content_type='text/plan')
            else:
                # inserting data in table class model
                entry = Job_application(candidate_name=name, candidate_cnic=nic, candidate_phone_no=phone,
                                        candidate_email=email, candidate_experience=candidate_experience,
                                        date=datetime.now())
                # adding data to database
                db.session.add(entry)
                db.session.commit()

                # Use Response to send a custom response
                return Response("Application submitted successfully!", status=200, content_type='text/plain')

        return render_template("jobapply.html")
