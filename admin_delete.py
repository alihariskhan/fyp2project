from flask import redirect, request

from sql import db
from guard import Guard


class Call_delete:
    def delete(self, guard_id):
        if request.method == 'GET':
            guard_delete = Guard.query.filter_by(guard_id=guard_id).first()

            if guard_delete:
                db.session.delete(guard_delete)
                db.session.commit()
                return redirect('/guardlist')

            else:
                # Handle the case where a guard or a guard_select request was found
                return "No match found"
