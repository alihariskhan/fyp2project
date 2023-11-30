from flask import request, render_template, redirect, url_for, flash, Response
from flask_login import login_user
from werkzeug.exceptions import BadRequest, NotFound

from supervisor import Supervisor
from sql import db


class Supervisor_register:

    def supervisor_register(self):
        if request.method == 'POST':
            supervisor_id = request.form['username']
            password = request.form['password']
            name = request.form['name']
            nic = request.form['cnic']
            phone_no = request.form['phone_no']
            address = request.form['address']

            # Check if the username is already in use
            if Supervisor.query.filter_by(supervisor_id=supervisor_id).first():
                return render_template('supervisor_register.html', error='ID is already in use')

            # Create a new admin
            new_supervisor = Supervisor()
            new_supervisor.supervisor_id = supervisor_id
            new_supervisor.supervisor_name = name
            new_supervisor.set_password(password)
            new_supervisor.supervisor_cnic = nic
            new_supervisor.supervisor_phone_no = phone_no
            new_supervisor.supervisor_address = address

            # Add the new admin to the database
            db.session.add(new_supervisor)
            db.session.commit()

            return redirect(url_for('admindashboard'))

        return render_template('supervisor_register.html')

    def supervisor_unregister(self, _id):
        supervisor = Supervisor.query.get_or_404(_id)
        try:
            db.session.delete(supervisor)
            db.session.commit()
            return Response('Supervisor deleted successfully', status=200, mimetype='text/plain')
        except Exception as e:
            db.session.rollback()
            return Response(f'Error: {str(e)}', status=500, mimetype='text/plain')
