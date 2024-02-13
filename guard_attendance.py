from flask import request, Response

# import Guard class
from guard import Guard
from sql import db


class GuardAttendance(db.Model):
    attendance_id = db.Column(db.Integer, primary_key=True)
    checkin_time = db.Column(db.DateTime, nullable=True)
    checkout_time = db.Column(db.DateTime, nullable=True)
    guard_id = db.Column(db.Integer, nullable=False)
    absent = db.Column(db.Boolean, default=False)

    def mark_attendance(self):
        try:
            if request.method == 'POST':
                guard_id = int(request.form['guard_id'])
                action = request.form['action']

                guard = Guard.query.get(guard_id)

                if guard:

                    if action == 'absent':
                        # Check if there's existing attendance for the guard on the current day
                        existing_attendance = GuardAttendance.query.filter(
                            GuardAttendance.guard_id == guard.guard_id,
                            GuardAttendance.absent == False).first()

                        if existing_attendance:
                            # Update the existing entry to mark the guard as absent
                            existing_attendance.absent = True
                            existing_attendance.checkin_time = None
                            existing_attendance.checkout_time = None
                            db.session.commit()
                            return Response(f'{guard.guard_name}{guard.guard_id} marked as absent for today',
                                            status=200,
                                            content_type='text/plain')

                        else:
                            # Create a new entry if no existing attendance for the guard on the current day
                            attendance = GuardAttendance(guard_id=guard.guard_id, absent=True)
                            db.session.add(attendance)
                            db.session.commit()
                            return Response(f'{guard.guard_name} marked as absent for today', status=200,
                                            content_type='text/plain')

                    elif action == 'checkin':
                        # Check if there's existing attendance for the guard on the current day
                        existing_attendance = GuardAttendance.query.filter(
                            GuardAttendance.absent == True).first()

                        if existing_attendance:
                            # Update the existing entry to record the check-in time
                            checkintime = request.form.get('checkintime')
                            existing_attendance.checkin_time = checkintime
                            existing_attendance.absent = False  # Set absent to False when check-in is recorded
                            db.session.commit()
                            return Response(f'Check-in recorded for {guard.guard_name}', status=200,
                                            content_type='text/plain')
                        else:
                            checkintime = request.form.get('checkintime')
                            # Create a new entry if no existing attendance for the guard on the current day
                            attendance = GuardAttendance(guard_id=guard.guard_id, checkin_time=checkintime)
                            db.session.add(attendance)
                            db.session.commit()
                            return Response(f'Check-in recorded for {guard.guard_name}', status=200,
                                            content_type='text/plain')

                    elif action == 'checkout':
                        last_attendance = GuardAttendance.query.filter_by(guard_id=guard.guard_id,
                                                                          checkout_time=None).first()

                        if last_attendance:
                            checkouttime = request.form.get('checkouttime')
                            last_attendance.checkout_time = checkouttime
                            db.session.commit()
                            return Response(f'Check-out recorded for {guard.guard_name}', status=200,
                                            content_type='text/plain')
                        else:
                            return Response(f'No active check-in found for {guard.guard_name}', status=404,
                                            content_type='text/plain')

                return Response('Guard not found', status=404, content_type='text/plain')

            return Response('Invalid request method', status=405, content_type='text/plain')

        except Exception as e:
            print(f"Error: {str(e)}")
            return Response('Internal Server Error', status=500, content_type='text/plain')
