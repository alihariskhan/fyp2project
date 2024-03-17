from flask import request, render_template
from sql import db
from client import Client


class Signup:
    def sign_up(self):
        if request.method == 'POST':
            name = request.form['name']
            cnic = request.form.get('cnic')
            address = request.form.get('address')
            phone_no = request.form.get('phone_no')  # Corrected variable name
            password = request.form.get('password')

            # Create a new Client object
            entry = Client(client_name=name, client_cnic=cnic, client_address=address, client_phone_no=phone_no,
                                 password_hash=password)

            # Add the new client to the database session
            db.session.add(entry)

            # Commit the changes to the database
            db.session.commit()

            # Redirect or render a template indicating successful signup
            return render_template('login.html')

        # If the request method is not POST, render the signup form template
        return render_template('signup.html')
