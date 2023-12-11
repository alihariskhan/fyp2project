from flask import Flask, render_template, redirect, Response, request
from flask_login import LoginManager, login_required, logout_user, current_user
from datetime import datetime

from sqlalchemy import func

from call_approve import CallApprove
# classes import
from admin_delete import Call_delete
from call_editguard import Call_editguard
from callforinterview import CallForInterview
from guard import Guard
from job_application import Job_application
from sql import db
from call_decline import Call_decline
from interview_call import Interview_call
from setinterviewdate import Call_interviewDate
from contactedforinterview import Contactedforinterview
from admin import Admin
from client import Client
from admin_register import Admin_register
from supervisor import Supervisor
from guard_attendance import GuardAttendance
from supervisor_register import Supervisor_register
from schedule import Schedule
from client_guard_reservation import Client_Guard_Reservation
from set_reservation_details import Set_Reservation_Details
from client_delete import Client_delete
from login import Login
from location_details import location_Details
from guard_reservation import Guard_reservation
from incident_report import Incident_Report
from incident_guard import Incident_Guard

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:@localhost/fyp2"
app.config['SECRET_KEY'] = 'ali72377'
db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    # You can adjust this based on your models
    admin = Admin.query.get(user_id)
    client = Client.query.get(user_id)
    supervisor = Supervisor.query.get(user_id)

    if admin:
        return admin
    elif client:
        return client
    elif supervisor:
        return supervisor
    else:
        return None


def fetch_dashboard_data(admin_id, admin_name):
    # Assuming you have some data fetching logic based on the client_id
    # Replace this with your actual data fetching logic
    data = {
        'admin_id': admin_id,
        'admin_name': admin_name
    }
    return data


@app.route("/show_all_incident_report", methods=['GET', 'POST'])
@login_required
def show_all_incident_report():
    supervisor_id_exist = Supervisor.query.filter_by(supervisor_id=current_user.supervisor_id).first()
    if supervisor_id_exist:
        obj = Incident_Report()
        result = obj.show_all_incident_report()
        return result
    else:
        return "access denied"


@app.route("/search_incident_report", methods=['GET', 'POST'])
@login_required
def search_incident_report():
    supervisor_id_exist = Supervisor.query.filter_by(supervisor_id=current_user.supervisor_id).first()
    if supervisor_id_exist:
        obj = Incident_Report()
        result = obj.search_incident_report()
        return result
    else:
        return "access denied"


@app.route("/incident_report", methods=['GET', 'POST'])
@login_required
def incident_report():
    supervisor_id_exist = Supervisor.query.filter_by(supervisor_id=current_user.supervisor_id).first()
    if supervisor_id_exist:
        obj = Incident_Report()
        result = obj.incident_report()
        return result
    else:
        return "access denied"


@app.route("/show_attendance", methods=['GET', 'POST'])
@login_required
def show_attendance():
    if request.method == 'POST':
        guard_id = int(request.form['guard_id'])
        start_date = datetime.strptime(request.form['start_date'], '%Y-%m-%d').date()
        end_date = datetime.strptime(request.form['end_date'], '%Y-%m-%d').date()

        # Query the database for attendance records
        results = GuardAttendance.query.filter(
            GuardAttendance.guard_id == guard_id,
            func.date(GuardAttendance.checkin_time).between(start_date, end_date)
        ).all()

        return render_template('result_table.html', result=results)

    return render_template('show_attendance.html', guards=Guard.query.all())


@app.route("/set_reservation_details", methods=['GET', 'POST'])
@login_required
def set_reservation_details():
    obj = Set_Reservation_Details()
    result = obj.set_reservation_details()
    return result


@app.route("/reservation_details", methods=["GET"])
@login_required
def reservation_details():
    try:
        requests = (
            db.session.query(Client_Guard_Reservation, Guard)
            .select_from(Client_Guard_Reservation)
            .join(Guard, Client_Guard_Reservation.guard_id == Guard.guard_id)
            .filter(Client_Guard_Reservation.client_id == current_user.client_id)
            .filter(Client_Guard_Reservation.location_id.is_(None))
            .all()
        )
        distinct_guard_ids = (Client_Guard_Reservation.query
                              .filter(current_user.client_id == Client.client_id)
                              .filter(Client_Guard_Reservation.location_id.is_(None))
                              .distinct(Client_Guard_Reservation.guard_id)
                              .with_entities(Client_Guard_Reservation.guard_id)
                              .all())

        return render_template("set_reservation_details.html", requests=requests,
                               distinct_guard_ids=distinct_guard_ids)

    except Exception as e:
        return Response(f"Error: {str(e)}", status=500, mimetype="text/plain")


@app.route("/reservation_request", methods=['GET', 'POST'])
@login_required
def reservation_request():
    requests = (
        db.session.query(Client_Guard_Reservation, Guard_reservation)
        .select_from(Client_Guard_Reservation)
        .join(Guard_reservation, Client_Guard_Reservation.reservation_id == Guard_reservation.reservation_id)

        .all()
    )
    # requests = Client_Guard_Reservation.query.all()
    return render_template("reservation_requests.html", requests=requests)


@app.route("/guard_select/<string:_id>", methods=['GET', 'POST'])
@login_required
def guard_select(_id):
    obj = Client_Guard_Reservation()
    result = obj.guard_select(_id)
    return result


@app.route("/guard_reservation")
@login_required
def guard_reservation():
    guards = Guard.query.filter(~Guard.guard_id.in_(db.session.query(Client_Guard_Reservation.guard_id))).all()
    return render_template("guards.html", guards=guards)


# Route to set schedule
@app.route("/schedule")
@login_required
def schedule():
    guards = Guard.query.all()
    locations = location_Details.query.all()
    return render_template("set_schedule.html", guards=guards, locations=locations)


# Route to set schedule
@app.route("/set_schedule", methods=['POST'])
@login_required
def set_schedule():
    obj = Schedule()
    result = obj.Set_schedule()
    return result


@app.route("/mark_attendance", methods=['POST', 'GET'])
@login_required
def mark_attendance():
    obj = GuardAttendance()
    result = obj.mark_attendance()
    return result


@app.route("/guardattendance")
@login_required
def guardattendance():
    guards = Guard.query.all()
    return render_template('guard_attendance.html', guards=guards)


@app.route('/admin/unregister', methods=['GET'])
@login_required
def admin_unreg():
    admin = Admin.query.all()

    return render_template('admin_unregister.html', admins=admin)


# Unregistration route for supervisor by admin
@app.route('/admin/delete/<string:_id>', methods=['GET', 'POST'])
@login_required
def admin_unregister(_id):
    obj = Admin_register()
    result = obj.admin_unregister(_id)
    return result


@app.route('/supervisor/unregister', methods=['GET'])
@login_required
def supervisor_unreg():
    supervisor = Supervisor.query.all()
    return render_template('supervisor_unregister.html', supervisors=supervisor)


# Unregistration route for supervisor by admin
@app.route('/supervisor/delete/<string:_id>', methods=['GET', 'POST'])
@login_required
def supervisor_unregister(_id):
    obj = Supervisor_register()
    result = obj.supervisor_unregister(_id)
    return result


# Registration route for supervisor by admin
@app.route('/supervisor/register', methods=['GET', 'POST'])
@login_required
def supervisor_register():
    obj = Supervisor_register()
    result = obj.supervisor_register()
    return result


# Registration route for admins
@app.route('/admin/register', methods=['GET', 'POST'])
@login_required
def admin_register():
    obj = Admin_register()
    result = obj.admin_register()
    return result


# Client login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    obj = Login()
    result = obj.login()
    return result


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/login')


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/services')
def services():
    return render_template('services.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')


# route to edit guarc details
@app.route("/editguard/<string:id>", methods=['GET', 'POST'])
@login_required
def editguard(id):
    obj = Call_editguard()

    result = obj.editguard(id)
    return result


# route to delete any guard from list
@app.route("/client_delete/<int:guard_id>", methods=['GET'])
@login_required
def client_delete(guard_id):
    obj = Client_delete()

    result = obj.delete(guard_id)
    return result


# route to delete any guard from list
@app.route("/delete/<int:guard_id>", methods=['GET'])
@login_required
def delete(guard_id):
    obj = Call_delete()

    result = obj.delete(guard_id)
    return result


# route to see guards list
@app.route("/guardlist")
@login_required
def guardlist():
    lists = Guard.query.filter_by().all()

    return render_template("guardlist.html", lists=lists)


# route to see Contacted applicants for interview by admin
@app.route("/interviewtimings")
@login_required
def interviewtimings():
    requests = Contactedforinterview.query.all()
    return render_template("interviewtimings.html", requests=requests)


# route to assign interview date to applicants by supervisor
@app.route("/setinterviewdate/<string:id>", methods=['GET', 'POST'])
@login_required
def interviewdate(id):
    obj = Call_interviewDate()
    result = obj.interviewdate(id)
    return result


# route to see interviewee by supervisor which are selected by admin to interview
@app.route("/admincalled")
@login_required
def admincall():
    # getting all data from Interview table
    obj = CallForInterview()
    requests = obj.query.filter_by().all()
    return render_template("admincalled.html", requests=requests)


# route to approve interviewee after passing interview
@app.route("/approve/<string:id>", methods=['GET', 'POST'])
@login_required
def approve(id):
    obj = CallApprove()

    result = obj.approve(id)
    return result


# route to call applicants to interview by admin. (Details will forward to supervisor, then supervisor will call by
# phone and email)
@app.route("/call/<string:_id>", methods=['GET', 'POST'])
@login_required
def call(_id):
    obj = Interview_call()
    result = obj.call(_id)
    return result


# route to decline application of applicants or interviewee by admin
@app.route("/decline/<string:_id>", methods=['GET', 'POST'])
@login_required
def decline(_id):
    obj = Call_decline()
    result = obj.decline(_id)
    return result


# Route of see Job Requests by Admin
@app.route("/jobrequests")
@login_required
def job_requests():
    # fetching data from database
    requests = Job_application.query.all()

    return render_template("jobrequests.html", requests=requests)


# Route of Supervisor Dashboard
@app.route("/supervisordashboard")
@login_required
def supervisor_dashboard():
    return render_template("supervisordashboard.html")


@app.route('/client_dashboard')
@login_required
def client_dashboard():
    return render_template('client_dashboard.html')


# Route of Admin Dashboard
@app.route("/admindashboard")
@login_required
def admin_dashboard():
    data = fetch_dashboard_data(current_user.admin_id, current_user.admin_name)
    requests = Job_application.query.order_by(Job_application.applicant_id.desc()).limit(10).all()
    guard_count = Guard.query.count()
    job_count = Job_application.query.count()
    client_count = Client.query.count()
    if guard_count < 1:
        guard_count = 0

    if job_count < 1:
        job_count = 0

    if client_count < 1:
        client_count = 0

    return render_template("admindashboard.html", requests=requests, guard_count=guard_count, job_count=job_count,
                           data=data, client_count=client_count)


# Route to apply for job
@app.route("/jobapply", methods=['GET', 'POST'])
def job_apply():
    obj = Job_application()
    result = obj.Call_job_apply()

    return result


if __name__ == '__main__':
    app.run(debug=True)
