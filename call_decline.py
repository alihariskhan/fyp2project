from datetime import datetime

from flask import request, redirect, url_for

from interview import Interview, Interview_History
from job_application import Job_application, Job_application_History
from sql import db


class Call_decline:

    def decline(self, _id):
        if request.method == 'GET':
            # filtering by id
            applicant = Job_application.query.filter_by(applicant_id=_id).first()

            # query to get the rows to delete
            delete_request = (db.session.query(Job_application, Interview)
                              .select_from(Job_application)
                              .join(Interview,
                                    Job_application.applicant_id == Interview.applicant_id)
                              .filter(Job_application.applicant_id == _id)
                              .all())

            # use url_for to generate the correct URLs
            decline_application_url = url_for('decline_application', _id=_id)
            decline_interview_url = url_for('decline_interview', _id=_id)

            # check which page is requesting e.g interviewee page or job request page
            if request.path == decline_application_url:

                history_entry = Job_application_History(applicant_id=applicant.applicant_id,
                                                        candidate_cnic=applicant.candidate_cnic,
                                                        candidate_phone_no=applicant.candidate_phone_no,
                                                        candidate_name=applicant.candidate_name,
                                                        date=applicant.date, candidate_email=applicant.candidate_email,
                                                        candidate_experience=applicant.candidate_experience,
                                                        timestamp=datetime.now(), interview_operation=False,
                                                        application_operation=True)
                # adding into job application history
                db.session.add(history_entry)

                # delete from job application table
                db.session.delete(applicant)
                db.session.commit()

                return redirect('/jobrequests')

            elif request.path == decline_interview_url:

                for job_application, interview in delete_request:
                    history_entry = Job_application_History(applicant_id=job_application.applicant_id,
                                                            candidate_cnic=job_application.candidate_cnic,
                                                            candidate_phone_no=job_application.candidate_phone_no,
                                                            candidate_name=job_application.candidate_name,
                                                            date=job_application.date,
                                                            candidate_email=job_application.candidate_email,
                                                            candidate_experience=job_application.candidate_experience,
                                                            timestamp=datetime.now(), interview_operation=True,
                                                            application_operation=False)

                    db.session.add(history_entry)
                    db.session.commit()

                    history_entry2 = Interview_History(id=interview.interview_id,
                                                       applicant_id=job_application.applicant_id,
                                                       date=interview.date, time=interview.time)

                    db.session.add(history_entry2)

                    db.session.delete(job_application)
                    db.session.delete(interview)

                # commit the changes
                db.session.commit()
                print("2nd  condition")

                return redirect('/interviewtimings')
            else:
                # Handle the case where neither an applicant, contacted nor an interviewee request was found
                return "no match found"

        db.session.commit()
