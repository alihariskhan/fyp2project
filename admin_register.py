from flask import request, render_template, redirect, url_for, Response

from admin import Admin
from sql import db


class Admin_register:

    def admin_register(self):
        if request.method == 'POST':
            admin_id = request.form['username']
            password = request.form['password']
            name = request.form['name']

            # Check if the username is already in use
            if Admin.query.filter_by(admin_id=admin_id).first():
                return render_template('admin_register.html', error='ID is already in use')

            # Create a new admin
            new_admin = Admin()
            new_admin.admin_id = admin_id
            new_admin.admin_name = name
            new_admin.set_password(password)

            # Add the new admin to the database
            db.session.add(new_admin)
            db.session.commit()



            return redirect(url_for('admindashboard'))

        return render_template('admin_register.html')

    def admin_unregister(self, _id):
        admin = Admin.query.get_or_404(_id)
        try:
            db.session.delete(admin)
            db.session.commit()
            return Response('Admin deleted successfully', status=200, mimetype='text/plain')
        except Exception as e:
            db.session.rollback()
            return Response(f'Error: {str(e)}', status=500, mimetype='text/plain')

