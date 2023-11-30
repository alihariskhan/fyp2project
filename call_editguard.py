from flask import request, redirect, render_template
from sql import db
from guard import Guard

class Call_editguard:
    def editguard(self, id):
        # Filter guard by id
        guard = Guard.query.filter_by(guard_id=id).first()

        # Check if the request method is POST
        if request.method == 'POST':
            name = request.form.get('guard_name')
            nic = request.form.get('guard_cnic')
            phone = request.form.get('guard_phone')
            email = request.form.get('email')
            experience = request.form.get('experience')
            date = request.form.get('date')

            # updating values
            #guard(guard_name=name, guard_cnic=nic, guard_phone=phone, guard_email=email, experience=experience)
            guard.guard_name = name
            guard.guard_cnic = nic
            guard.guard_phone = phone
            guard.guard_email = email
            guard.date = date
            guard.experience = experience


            db.session.commit()

            return redirect('/guardlist')

        return render_template('editguard.html', guard=guard, id=id)
