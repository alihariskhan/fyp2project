from datetime import datetime, time

from flask import request
from flask_login import current_user
from sqlalchemy import text

from client import Client
from sql import db
from client_guard_reservation import Client_Guard_Reservation
from guard_reservation import Guard_reservation
from location_details import location_Details


class Set_Reservation_Details:
    def set_reservation_details(self):
        try:
            # Step 1: Add entry to location_details table
            form_data = {
                'location': request.form['location'].strip(),
                'start_date': request.form['start_date'],
                'end_date': request.form['end_date'],
                'start_time': request.form['duty_start_time'],
                'end_time': request.form['duty_end_time'],
                'schedule_details': request.form['schedule_details'],
                'duty_shift': request.form['shiftselect']
            }
            print("Form Data:", form_data)

            # if client requires guards on same timing and same location
            condition1 = (form_data['location'].strip() and form_data['start_time'] != time(0, 0, 0)
                          and form_data['end_time'] != time(0, 0, 0)
                          and form_data['duty_shift'] != "null")

            # if client requires guards on same timing but different locations
            condition2 = (form_data['location'].strip() == '' and form_data['start_time'] != time(0, 0, 0)
                          and form_data['end_time'] != time(0, 0, 0)
                          and form_data['duty_shift'] != "null")

            # if client requires guards on same locations but different timings
            condition3 = (form_data['location'].strip() and form_data['start_time'] == ''
                          and form_data['end_time'] == '' and form_data['duty_shift'] == "null")

            # if client requires guards on different timing and different locations
            condition4 = (form_data['location'].strip() == '' and form_data['start_time'] == ''
                          and form_data['end_time'] == ''
                          and form_data['duty_shift'] == "null")

            print("Condition 1:", condition1)
            print("Condition 2:", condition2)
            print("Condition 3:", condition3)
            print("Condition 4:", condition4)

            if condition1:

                entry = location_Details(location=form_data['location'])
                db.session.add(entry)
                db.session.commit()

                entry_guard_reservation = Guard_reservation(res_datetime=datetime.now(),
                                                            start_date=form_data['start_date'],
                                                            end_date=form_data['end_date'],
                                                            schedule_details=form_data['schedule_details'])
                db.session.add(entry_guard_reservation)
                db.session.commit()

                requests = (Client_Guard_Reservation.query.filter(
                    Client_Guard_Reservation.client_id == current_user.client_id)
                            .filter(Client_Guard_Reservation.location_id.is_(None))
                            .filter(Client_Guard_Reservation.reservation_id.is_(None))).all()

                for request_entry in requests:
                    request_entry.duty_shift = form_data['duty_shift']
                    request_entry.start_time = form_data['start_time']
                    request_entry.end_time = form_data['end_time']
                    db.session.commit()

                # Retrieve the generated ids
                location_id = entry.location_id
                reservation_id = entry_guard_reservation.reservation_id

                # Step 3: Update corresponding Guard_Select entries with location_id
                guard_entries_to_update = (
                    Client_Guard_Reservation.query
                    .filter_by(client_id=current_user.client_id, location_id=None, reservation_id=None)
                    .all()
                )

                # Update all entries in a single query
                if guard_entries_to_update:
                    # Use a list comprehension to extract IDs
                    guard_ids = [entry.guard_id for entry in guard_entries_to_update]

                    # Update entries with the generated location_id
                    sql_query = text("UPDATE client_guard_reservation SET location_id = :location_id, "
                                     "reservation_id = :reservation_id WHERE guard_id IN :guard_ids")
                    db.session.execute(sql_query, {"location_id": location_id, "reservation_id": reservation_id,
                                                   "guard_ids": guard_ids})
                    db.session.commit()
                return '{"success": true}'

            elif condition2:

                entry_guard_reservation = Guard_reservation(res_datetime=datetime.now(),
                                                            start_date=form_data['start_date'],
                                                            end_date=form_data['end_date'],
                                                            schedule_details=form_data['schedule_details'])
                db.session.add(entry_guard_reservation)
                db.session.commit()

                requests = (Client_Guard_Reservation.query.filter(
                    Client_Guard_Reservation.client_id == current_user.client_id)
                            .filter(Client_Guard_Reservation.location_id.is_(None))
                            .filter(Client_Guard_Reservation.reservation_id.is_(None))).all()

                for request_entry in requests:
                    request_entry.duty_shift = form_data['duty_shift']
                    request_entry.start_time = form_data['start_time']
                    request_entry.end_time = form_data['end_time']
                    db.session.commit()

                distinct_guard_ids = (Client_Guard_Reservation.query
                                      .filter(current_user.client_id == Client.client_id)
                                      .filter(Client_Guard_Reservation.location_id.is_(None))
                                      .distinct(Client_Guard_Reservation.guard_id)
                                      .with_entities(Client_Guard_Reservation.guard_id)
                                      .all())

                for guard_id_tuple in distinct_guard_ids:
                    guard_id = guard_id_tuple[0]
                    location = request.form.get(f'{guard_id}_location')

                    entry = location_Details(location=location)
                    db.session.add(entry)
                    db.session.commit()

                    requests = Client_Guard_Reservation.query.filter_by(guard_id=guard_id).first()
                    requests.location_id = entry.location_id
                    db.session.commit()

                # Retrieve the generated ids
                reservation_id = entry_guard_reservation.reservation_id

                # Step 3: Update corresponding Guard_Select entries with location_id
                guard_entries_to_update = (
                    Client_Guard_Reservation.query
                    .filter_by(client_id=current_user.client_id, reservation_id=None)
                    .all()
                )

                # Update all entries in a single query
                if guard_entries_to_update:
                    # Use a list comprehension to extract IDs
                    guard_ids = [entry.guard_id for entry in guard_entries_to_update]

                    # Update entries with the generated location_id
                    sql_query = text("UPDATE client_guard_reservation SET  "
                                     "reservation_id = :reservation_id WHERE guard_id IN :guard_ids")
                    db.session.execute(sql_query, {"reservation_id": reservation_id,
                                                   "guard_ids": guard_ids})
                    db.session.commit()
                return '{"success": true2}'

            elif condition3:

                entry = location_Details(location=form_data['location'])
                db.session.add(entry)
                db.session.commit()

                entry_guard_reservation = Guard_reservation(res_datetime=datetime.now(),
                                                            start_date=form_data['start_date'],
                                                            end_date=form_data['end_date'],
                                                            schedule_details=form_data['schedule_details'])

                db.session.add(entry_guard_reservation)
                db.session.commit()

                distinct_guard_ids = (Client_Guard_Reservation.query
                                      .filter(current_user.client_id == Client.client_id)
                                      .filter(Client_Guard_Reservation.location_id.is_(None))
                                      .distinct(Client_Guard_Reservation.guard_id)
                                      .with_entities(Client_Guard_Reservation.guard_id)
                                      .all())

                for guard_id_tuple in distinct_guard_ids:
                    guard_id = guard_id_tuple[0]
                    duty_shift = request.form.get(f'{guard_id}_shiftselect')
                    duty_start_time = request.form.get(f'{guard_id}_duty_start_time')
                    duty_end_time = request.form.get(f'{guard_id}_duty_end_time')

                    requests = Client_Guard_Reservation.query.filter_by(guard_id=guard_id).first()

                    requests.duty_shift = duty_shift
                    requests.start_time = duty_start_time
                    requests.end_time = duty_end_time
                    db.session.commit()

                # Retrieve the generated ids
                location_id = entry.location_id
                reservation_id = entry_guard_reservation.reservation_id

                # Step 3: Update corresponding Guard_Select entries with location_id
                guard_entries_to_update = (
                    Client_Guard_Reservation.query
                    .filter_by(client_id=current_user.client_id, reservation_id=None)
                    .all()

                )

                # Update all entries in a single query
                if guard_entries_to_update:
                    # Use a list comprehension to extract IDs
                    guard_ids = [entry.guard_id for entry in guard_entries_to_update]

                    # Update entries with the generated location_id
                    sql_query = text("UPDATE client_guard_reservation SET location_id = :location_id, "
                                     "reservation_id = :reservation_id WHERE guard_id IN :guard_ids")
                    db.session.execute(sql_query, {"location_id": location_id, "reservation_id": reservation_id,
                                                   "guard_ids": guard_ids})

                    db.session.commit()

                return '{"success": true3}'

            elif condition4:
                start_date = request.form['start_date']
                end_date = request.form['end_date']
                schedule_details = request.form['schedule_details']

                distinct_guard_ids = (Client_Guard_Reservation.query
                                      .filter(current_user.client_id == Client.client_id)
                                      .filter(Client_Guard_Reservation.location_id.is_(None))
                                      .distinct(Client_Guard_Reservation.guard_id)
                                      .with_entities(Client_Guard_Reservation.guard_id)
                                      .all())

                for guard_id_tuple in distinct_guard_ids:
                    guard_id = guard_id_tuple[0]
                    duty_shift = request.form.get(f'{guard_id}_shiftselect')
                    duty_start_time = request.form.get(f'{guard_id}_duty_start_time')
                    duty_end_time = request.form.get(f'{guard_id}_duty_end_time')
                    location = request.form.get(f'{guard_id}_location')

                    requests = Client_Guard_Reservation.query.filter_by(guard_id=guard_id).first()

                    requests.duty_shift = duty_shift
                    requests.start_time = duty_start_time
                    requests.end_time = duty_end_time
                    db.session.commit()

                    entry = location_Details(location=location)
                    db.session.add(entry)
                    db.session.commit()

                    requests.location_id = entry.location_id
                    db.session.commit()

                entry = Guard_reservation(res_datetime=datetime.now(), start_date=start_date, end_date=end_date,
                                          schedule_details=schedule_details)

                db.session.add(entry)
                db.session.commit()

                reservation_id = entry.reservation_id

                guard_entries_to_update = (
                    Client_Guard_Reservation.query
                    .filter_by(client_id=current_user.client_id, reservation_id=None)
                    .all()
                )
                if guard_entries_to_update:
                    # Use a list comprehension to extract IDs
                    guard_ids = [entry.guard_id for entry in guard_entries_to_update]

                    # Update entries with the generated location_id
                    sql_query = text("UPDATE client_guard_reservation SET  "
                                     "reservation_id = :reservation_id WHERE guard_id IN :guard_ids")
                    db.session.execute(sql_query, {"reservation_id": reservation_id,
                                                   "guard_ids": guard_ids})
                    db.session.commit()

                    # Return a simple JSON-formatted string
                return '{"success": true4}'
            else:
                return '{"success": false, "condition not matched"}'

        except Exception as e:
            print(f"Error: {str(e)}")
            # Rollback the transaction in case of an error
            db.session.rollback()
            # Return a simple JSON-formatted string with the error
            return f'{{"success": false, "error": "{str(e)}"}}'
