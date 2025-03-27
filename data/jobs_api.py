from flask import Blueprint, jsonify, make_response

from . import db_session
from .jobs import Jobs


jobs_api = Blueprint("jobs_api",
                     __name__,
                     template_folder="templates")


@jobs_api.route("/api/jobs/")
def get_jobs():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).all()
    return jsonify(
        {"jobs": [job.to_dict() for job in jobs]}
    )


@jobs_api.route("/api/jobs/<int:job_id>")
def get_job(job_id):
    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).get(job_id)
    if not job:
        return make_response(jsonify({'error': 'Not found'}), 404)
    return jsonify(
        {"jobs": [job.to_dict()]}
    )