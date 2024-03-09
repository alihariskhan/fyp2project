from flask import request, redirect, flash, render_template
from flask_login import login_user

from admin import authenticate_admin
from client import authenticate_client
from guard import authenticate_guard
from supervisor import authenticate_supervisor


class Login:
    def login(self):
        if request.method == 'POST':
            _id = request.form.get('username')
            password = request.form.get('password')

            admin = authenticate_admin(_id, password)
            client = authenticate_client(_id, password)
            supervisor = authenticate_supervisor(_id, password)
            guard = authenticate_guard(_id, password)

            if admin:
                login_user(admin)
                return redirect('/admindashboard')
            elif client:
                login_user(client)
                return redirect('/client_dashboard')
            elif supervisor:
                login_user(supervisor)
                return redirect('/supervisordashboard')
            elif guard:
                login_user(guard)
                return redirect('/guard_dashboard')

            else:
                flash(f'Invalid username or password. Please try again.{password}', 'danger')

        return render_template('login.html')
