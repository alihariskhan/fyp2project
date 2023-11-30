from flask import request

from sql import db


class Schedule(db.Model):
    schedule_id = db.Column(db.Integer, primary_key=True)
    guard_id = db.Column(db.Integer, nullable=False)
    duty_shift = db.Column(db.String, nullable=False)
    location = db.Column(db.String, nullable=False)
    start_date = db.Column(db.String, nullable=False)
    end_date = db.Column(db.String, nullable=False)
    start_time = db.Column(db.String, nullable=False)
    end_time = db.Column(db.String, nullable=False)
    schedule_details = db.Column(db.String, nullable=False)

    def Set_schedule(self):
        if request.method == 'POST':
            # Handle regular form submission
            guard_id = request.form.get('guard_id')
            print(f"Fetching record for guard_id: {guard_id}")
            shift_select = request.form.get('shiftselect')
            print(f"Fetching record for shift: {shift_select}")
            location = request.form.get('location')
            manual_location = request.form['manual_location']
            start_date = request.form['start_date']
            end_date = request.form['end_date']
            start_time = request.form['start_time']
            end_time = request.form['end_time']
            schedule_details = request.form['schedule_details']

            try:
                if location.strip() and manual_location.strip():
                    return 'double location'

                elif location.strip():
                    guard = (Schedule.query.filter(guard_id=guard_id)
                             .filter(start_date=start_date)
                             .filter(start_time=start_time))
                    if guard:
                        return 'exist'
                    else:
                        entry = Schedule(guard_id=guard_id, duty_shift=shift_select, location=location,
                                         start_date=start_date, end_date=end_date, start_time=start_time, end_time=end_time,
                                         schedule_details=schedule_details)

                        db.session.add(entry)
                        db.session.commit()
                        return 'success'

                elif manual_location.strip():
                    guard = (Schedule.query.filter(guard_id=guard_id)
                             .filter(start_date=start_date)
                             .filter(start_time=start_time))
                    if guard:
                        return 'exist'
                    else:
                        entry = Schedule(guard_id=guard_id, duty_shift=shift_select, location=manual_location,
                                         start_date=start_date, end_date=end_date, start_time=start_time,
                                         end_time=end_time,
                                         schedule_details=schedule_details)
                        db.session.add(entry)
                        db.session.commit()
                        return 'success location manually'

            except Exception as e:
                print(f"Error: {str(e)}")
                # Rollback the transaction in case of an error
                db.session.rollback()
                # Return a simple JSON-formatted string with the error
                return f'{{"success": false, "error": "{str(e)}"}}'
        else:
            # Handle AJAX request
            return 'Invalid request method'
