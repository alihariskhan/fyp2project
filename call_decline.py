from flask import request, redirect
from sql import db
from job_application import Job_application
from contactedforinterview import Contactedforinterview


class Call_decline:

    def decline(self, id):
        if request.method == 'GET':
            # filtering by id
            applicant = Job_application.query.filter_by(applicant_id=id).first()

            # filtering by id
            contacted = Contactedforinterview.query.filter_by(interviewee_id=id).first()

            # check which page is requesting e.g interviewee page or job request page
            if applicant:
                db.session.delete(applicant)
                db.session.commit()
                return redirect('/jobrequests')

            elif contacted:
                db.session.delete(contacted)
                db.session.commit()
                return redirect('/interviewtimings')
            else:
                # Handle the case where neither an applicant, contacted nor an interviewee request was found
                return "no match found"

        db.session.commit()