from flask import request, jsonify
from flask_login import current_user

from location_details import location_Details
from client_guard_reservation import Client_Guard_Reservation
from gps_tracking import Gps_Tracking
from guard import Guard
from sql import db


class Get_Location:
    def get_location(self):
        try:
            # Get the selected guard ID from the request parameters
            selected_guard_id = request.args.get('guard_id')

            # Query the specific guard location from the gps_tracking table
            guard = Gps_Tracking.query.filter_by(guard_id=selected_guard_id).first()

            if guard is not None:
                # If data exists in gps_tracking table, use it
                location = (db.session.query(Client_Guard_Reservation, Guard, location_Details)
                            .select_from(Client_Guard_Reservation)
                            .join(Guard, Client_Guard_Reservation.guard_id == Guard.guard_id)
                            .join(location_Details, Client_Guard_Reservation.location_id == location_Details.location_id)
                            .filter(Client_Guard_Reservation.guard_id == selected_guard_id)
                            .first()
                            )

                if location is not None:
                    guard_data = {
                        'guard_id': guard.guard_id,
                        'latitude': guard.latitude,
                        'longitude': guard.longitude,
                        'start_lat': guard.start_lat,
                        'start_long': guard.start_long,
                        'start_time': guard.start_time,
                        'stop_time': guard.stop_time,
                        'location': location.location_Details.location if location.location_Details else None
                    }
                    print(f"guard data: {guard_data}, location: {location.location_Details.location}")
                    return jsonify(guard_data)

            # If no data in gps_tracking table, fetch data from location_details table
            location_only = (db.session.query(Client_Guard_Reservation, location_Details)
                             .select_from(Client_Guard_Reservation)
                             .join(location_Details, Client_Guard_Reservation.location_id == location_Details.location_id)
                             .filter(Client_Guard_Reservation.guard_id == selected_guard_id)
                             .first()
                             )

            if location_only is not None:
                location_data = {
                    'guard_id': selected_guard_id,
                    'location': location_only.location_Details.location if location_only.location_Details else None
                }
                print(f"location data: {location_data}")
                return jsonify(location_data)

            # Return an empty response if no guard is selected or found
            return jsonify({})

        except Exception as e:
            # Handle exceptions, log, or return an error response
            print(f"Error fetching guard location: {str(e)}")
            return jsonify({'error': 'Internal Server Error'}), 500


