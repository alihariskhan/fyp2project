from flask import request, redirect
from contactedforinterview import Contactedforinterview
from guard import Guard
from sql import db
from datetime import datetime

class CallApprove:
    def approve(self,id):
        # getting data from interview table
        guard = Contactedforinterview.query.filter_by(interviewee_id=id).first()
        if request.method == 'GET':
            name = guard.interviewee_name
            nic = guard.interviewee_cnic
            phone = guard.interviewee_phone_no
            email = guard.interviewee_email
            experience = guard.experience


            # inserting data into database class model
            entry = Guard(guard_name=name, guard_cnic=nic, guard_phone=phone, guard_email=email, date=datetime.now(),
                          experience=experience)

            # adding data to database
            db.session.add(entry)
            db.session.commit()

            # selecting data by filtering id
            deletereq = Contactedforinterview.query.filter_by(interviewee_id=id).first()

            # delete from database
            db.session.delete(deletereq)
            db.session.commit()

            return redirect('/interviewtimings')


