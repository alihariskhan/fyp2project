from flask import render_template, request, redirect

from callforinterview import CallForInterview
from contactedforinterview import Contactedforinterview
from sql import db


class Call_interviewDate:
    def interviewdate(self, id):
        # getting applicants filter by id
        obj = CallForInterview()
        requests = obj.query.filter_by(interviewer_id=id).first()
        if request.method == 'POST':
            # storing values in temporary variables
            _id = requests.interviewer_id
            name = requests.interviewer_name
            nic = requests.interviewer_cnic
            phone = requests.interviewer_phone_no
            email = requests.interviewer_email
            date = request.form.get('date')
            remarks = request.form.get('remarks')
            experience = requests.experience

            # inserting data into database class model
            entry = Contactedforinterview(interviewee_id=_id, interviewee_name=name, interviewee_cnic=nic,
                                          interviewee_phone_no=phone, interviewee_email=email, date=date,
                                          remarks=remarks, experience=experience)

            # adding values to database
            db.session.add(entry)
            db.session.commit()
            # deleting
            deletereq = obj.query.filter_by(interviewer_id=id).first()
            db.session.delete(deletereq)
            db.session.commit()
            return redirect("/admincalled")

        return render_template("setinterviewdate.html", id=id)
