from flask import Blueprint, jsonify, make_response, request
from datetime import datetime

from . import db_session
from .jobs import Jobs


jobs_api = Blueprint("jobs_api",
                     __name__,
                     template_folder="templates")


@jobs_api.route("/api/jobs/")
def get_jobs():
    db_sess = db_session.create_session()

    jobs = db_sess.query(Jobs).all()

    return jsonify({"jobs": [job.to_dict() for job in jobs]})


@jobs_api.route("/api/jobs/<int:job_id>")
def get_job(job_id):
    db_sess = db_session.create_session()

    job = db_sess.query(Jobs).get(job_id)

    if not job:
        return make_response(jsonify({'error': 'Not found'}), 404)

    return jsonify({"jobs": [job.to_dict()]})


@jobs_api.route("/api/jobs/", methods=["POST"])
def create_job():
    if not request.json:
        return make_response(jsonify({'error': 'Empty request'}), 400)
    
    allowed_fields = ["id", "team_leader_id", "job", "work_size", "collaborators", "is_finished"]

    if not all(key in request.json for key in allowed_fields):
        return make_response(jsonify({'error': 'Missing fields'}), 400)

    db_sess = db_session.create_session()

    start_date = request.json.get("start_date")

    if start_date:
        start_date = datetime.fromisoformat(start_date)

    send_date = request.json.get("end_date")

    if send_date:
        send_date = datetime.fromisoformat(send_date)

    job = Jobs(
        id=request.json["id"],
        team_leader_id=request.json["team_leader_id"],
        job=request.json["job"],
        work_size=request.json["work_size"],
        collaborators=request.json["collaborators"],
        start_date=start_date,
        send_date=send_date,
        is_finished=request.json["is_finished"],
    )

    if db_sess.query(Jobs).filter(Jobs.id == job.id).first():
        return make_response(jsonify({'error': 'Id already exists'}), 400)

    db_sess.add(job)
    db_sess.commit()

    return jsonify({'success': 'OK'})


@jobs_api.route("/api/jobs/<int:job_id>", methods=["DELETE"])
def delete_job(job_id):
    db_sess = db_session.create_session()

    job = db_sess.query(Jobs).get(job_id)

    if not job:
        return make_response(jsonify({'error': 'Not found'}), 404)

    db_sess.delete(job)
    db_sess.commit()

    return jsonify({'success': 'OK'})