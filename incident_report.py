from datetime import datetime

from flask import render_template, request, redirect
from sqlalchemy import func

from guard import Guard
from incident_guard import Incident_Guard
from location_details import location_Details
from sql import db


class Incident_Report(db.Model):
    __tablename__ = "incident_report"
    incident_id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    description = db.Column(db.String, nullable=False)
    timestamp = db.Column(db.String, nullable=False)
    location_id = db.Column(db.Integer, db.ForeignKey('location_details.location_id'), nullable=False)

    def incident_report(self):
        if request.method == 'POST':
            date = request.form['incident_date']
            time = request.form['incident_time']
            guard_ids = request.form.getlist('incident_guard')
            location_id = request.form['incident_location']
            description = request.form['description']

            entry = Incident_Report(date=date, time=time, description=description, timestamp=datetime.now(),
                                    location_id=location_id)
            db.session.add(entry)
            db.session.commit()

            incident_id = entry.incident_id

            for guard_id in guard_ids:
                entry2 = Incident_Guard(incident_id=incident_id, guard_id=guard_id)
                db.session.add(entry2)
            db.session.commit()

            return redirect('/incident_report')

        guards = Guard.query.all()
        locations = location_Details.query.all()
        return render_template("incident_report_form.html", guards=guards, locations=locations)

    def show_all_incident_report(self):
        results = (db.session.query(Incident_Report, Incident_Guard, location_Details, Guard)
                   .select_from(Incident_Report)
                   .join(Incident_Guard, Incident_Report.incident_id == Incident_Guard.incident_id)
                   .join(location_Details, Incident_Report.location_id == location_Details.location_id)
                   .join(Guard, Incident_Guard.guard_id == Guard.guard_id)
                   .all()
                   )

        return render_template("show_all_incident_report.html", results=results)

    def search_incident_report(self):
        if request.method == 'POST':
            start_date = request.form['start_date']
            end_date = request.form['end_date']
            incident_guard = request.form['incident_guard']
            incident_location = request.form['incident_location']

            condition1 = (incident_guard == '', incident_location == '')
            condition2 = (start_date == '', end_date == '', incident_location == '', incident_guard != '')
            condition3 = (start_date == '', end_date == '', incident_location != '', incident_guard == '')

            print(f"{start_date}, {end_date}, {incident_location}, {incident_guard}")
            if all(condition1):
                results = (db.session.query(Incident_Report, Incident_Guard, location_Details, Guard)
                           .select_from(Incident_Report)
                           .join(Incident_Guard, Incident_Report.incident_id == Incident_Guard.incident_id)
                           .join(location_Details, Incident_Report.location_id == location_Details.location_id)
                           .join(Guard, Incident_Guard.guard_id == Guard.guard_id)
                           .filter(func.date(Incident_Report.date).between(start_date, end_date))
                           .all()
                           )
                print("condition1")
                return render_template("searched_incident_report.html", results=results)

            elif all(condition2):
                guard_rows = db.session.query(Incident_Guard.incident_id).filter(
                    Incident_Guard.guard_id == incident_guard).distinct().all()

                # Extracting incident_ids from the result set
                incident_ids = [row.incident_id for row in guard_rows]

                # Now fetch all rows related to the incident_ids
                results = (
                    db.session.query(Incident_Report, Incident_Guard, location_Details, Guard)
                    .select_from(Incident_Report)
                    .join(Incident_Guard, Incident_Report.incident_id == Incident_Guard.incident_id)
                    .join(location_Details, Incident_Report.location_id == location_Details.location_id)
                    .join(Guard, Incident_Guard.guard_id == Guard.guard_id)
                    .filter(Incident_Report.incident_id.in_(incident_ids))
                    .all()
                )
                print("condition2")

                return render_template("searched_incident_report.html", results=results)

            elif all(condition3):
                results = (db.session.query(Incident_Report, Incident_Guard, location_Details, Guard)
                           .select_from(Incident_Report)
                           .join(Incident_Guard, Incident_Report.incident_id == Incident_Guard.incident_id)
                           .join(location_Details, Incident_Report.location_id == location_Details.location_id)
                           .join(Guard, Incident_Guard.guard_id == Guard.guard_id)
                           .filter(location_Details.location_id == incident_location)
                           .all()
                           )
                print("condition3")

                return render_template("searched_incident_report.html", results=results)
        guards = Guard.query.all()
        locations = location_Details.query.all()
        return render_template("search_incident_report.html", guards=guards, locations=locations)
