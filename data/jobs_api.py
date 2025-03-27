from flask import Blueprint, jsonify, request
from werkzeug.exceptions import NotFound

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
        raise NotFound()
    return jsonify(
        {"jobs": [job.to_dict()]}
    )


@jobs_api.errorhandler(404)
def not_found(error):
    return jsonify({"error": f"{error.name}. {error.description}"}), error.code


@jobs_api.errorhandler(400)
def not_found(error):
    return jsonify({"error": f"{error.name}. {error.description}"}), error.code