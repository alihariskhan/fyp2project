from datetime import datetime

from flask import request, redirect

from interview import Interview
from job_application import Job_application, Job_application_History
from guard import Guard
from sql import db


class CallApprove:
    def approve(self, _id):
        # getting data from interview table
        guard = Job_application.query.filter_by(applicant_id=_id).first()
        if request.method == 'GET':
            name = guard.candidate_name
            nic = guard.candidate_cnic
            phone = guard.candidate_phone_no
            email = guard.candidate_email
            experience = guard.candidate_experience
            date = guard.date

            # inserting data into database class model
            entry = Guard(guard_name=name, guard_cnic=nic, guard_phone=phone, guard_email=email, date=datetime.now(),
                          experience=experience)

            # adding data to database
            db.session.add(entry)
            db.session.commit()

            entry2 = Job_application_History(applicant_id=_id, candidate_name=name, candidate_cnic=nic,
                                             candidate_email=email, candidate_experience=experience, date=date,
                                             candidate_phone_no=phone, timestamp=datetime.now(),
                                             interview_operation=True, application_operation=False)

            db.session.add(entry2)
            db.session.commit()

            # query to get the rows to delete
            delete_request = (db.session.query(Job_application, Interview)
                              .select_from(Job_application)
                              .join(Interview, Job_application.applicant_id == Interview.applicant_id)
                              .filter(Job_application.applicant_id == _id)
                              .all())

            # delete each row individually
            for job_application, interview in delete_request:
                db.session.delete(job_application)
                db.session.delete(interview)

            # commit the changes
            db.session.commit()
            return redirect('/interviewtimings')
