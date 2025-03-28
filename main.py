from flask import Flask, render_template, redirect, request, abort, jsonify, make_response, url_for, make_response
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
import os
import requests
from flask_restful import Api

from data import db_session

from data.users import User
from data.jobs import Jobs
from data.departments import Department

from forms.users import RegisterForm, LoginForm
from forms.jobs import AddJobForm
from forms.departments import AddDepartmentForm

from data.users_api import users_api
from data.jobs_api import jobs_api

from data.users_resources import init_api_routes


def add_data_to_Base_of_Data():
    from data import samples
    samples.add_data_to_db()


app = Flask(__name__)
login_manager = LoginManager(app)
app.config["SECRET_KEY"] = "yandexlyceum_secret_key"
api = Api(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.get(User, user_id)


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = User(
            surname=form.surname.data,
            name=form.name.data,
            age=form.age.data,
            position=form.position.data,
            speciality=form.speciality.data,
            address=form.address.data,
            city_from=form.city_from,
            email=form.login.data,
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect("/login")
    return render_template("register.html", title="Регистрация", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template("login.html", title="Авторизация", form=form, message='Неверный пароль')
    return render_template("login.html", title="Авторизация", form=form, message='')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")



@app.route("/users_show/<int:user_id>")
def users_show(user_id):
    resp = requests.get(f'{request.host_url}{url_for("users_api.get_user", user_id=user_id)}')

    if not resp:
        return make_response(jsonify({'error': 'Not found'}), 404)
    
    user = resp.json()["users"][0]
    user_city = user["city_from"]

    geocoder_params = {
        "apikey": "8013b162-6b42-4997-9691-77b7074026e0",
        "geocode": user_city,
        "format": "json"
    }

    geocode_resp = requests.get("http://geocode-maps.yandex.ru/1.x/", params=geocoder_params)

    if not geocode_resp:
        return make_response(jsonify({'error': f"Ошибка geocoder. Статус: {geocode_resp.status_code}. {geocode_resp.reason}"}), 400)
    geocode_json = geocode_resp.json()

    try:
        point = geocode_json["response"]["GeoObjectCollection"]["featureMember"][0][
            "GeoObject"]["Point"]["pos"]
    except (KeyError, IndexError):
        return make_response(jsonify({'error': 'Not found'}), 404)

    point = ",".join(point.split())

    map_static_params = {
        "ll": point,
        "l": "sat",
        "z": 13,
    }

    map_url = requests.Request(url="https://static-maps.yandex.ru/1.x/",
                               params=map_static_params).prepare().url

    return render_template("user_city.html", user_data=user, map_url=map_url)


@app.route("/add-job", methods=["GET", "POST"])
@login_required
def add_job():
    form = AddJobForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        job = Jobs(
            job=form.job.data,
            team_leader_id=form.team_leader.data,
            work_size=form.work_size.data,
            collaborators=form.collaborators.data,
            is_finished=form.is_finished.data
        )
        db_sess.add(job)
        db_sess.commit()
        return redirect("/")
    return render_template("add_job.html", form=form, title="Adding a job")


@app.route("/edit-job/<int:job_id>", methods=["GET", "POST"])
@login_required
def edit_job(job_id):
    form = AddJobForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        job = db_sess.query(Jobs).filter(Jobs.id == job_id).filter((Jobs.team_leader == current_user)
                                                                   | (current_user.id == 1)).first()
        if job:
            form.team_leader.data = job.team_leader_id
            form.job.data = job.job
            form.work_size.data = job.work_size
            form.collaborators.data = job.collaborators
            form.is_finished.data = job.is_finished
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        job = db_sess.query(Jobs).filter(Jobs.id == job_id).filter((Jobs.team_leader == current_user)
                                                                   | (current_user.id == 1)).first()
        if job:
            job.team_leader_id = form.team_leader.data
            job.job = form.job.data
            job.work_size = form.work_size.data
            job.collaborators = form.collaborators.data
            job.is_finished = form.is_finished.data
            db_sess.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template("add_job.html", title="Изменение работы", form=form)


@app.route("/delete-job/<int:job_id>", methods=["GET", "POST"])
@login_required
def delete_job(job_id):
    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).filter(Jobs.id == job_id).filter((Jobs.team_leader == current_user)
                                                               | (current_user.id == 1)).first()
    if job:
        db_sess.delete(job)
        db_sess.commit()
    else:
        abort(404)
    return redirect("/")


@app.route("/add-department", methods=["GET", "POST"])
@login_required
def add_department():
    form = AddDepartmentForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        if db_sess.query(Department).filter(Department.email == form.email.data).first():
            return redirect("/add-department", message='Такой депортамент уже существует')
        department = Department(
            title=form.title.data,
            chief_id=form.chief_id.data,
            members=form.members.data,
            email=form.email.data,
        )
        db_sess.add(department)
        db_sess.commit()
        return redirect("/departments")
    return render_template("add_department.html", title="Добавить работу", form=form, message='')


@app.route("/edit-department/<int:department_id>", methods=["GET", "POST"])
@login_required
def edit_department(department_id):
    form = AddDepartmentForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        department = db_sess.query(Department).filter(Department.id == department_id).filter((Department.chief == current_user) | (current_user.id == 1)).first()
        if department:
            form.title.data = department.title
            form.chief_id.data = department.chief_id
            form.members.data = department.members
            form.email.data = department.email
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        department = db_sess.query(Department).filter(Department.id == department_id).filter((Department.chief == current_user) | (current_user.id == 1)).first()
        if department:
            department.title = form.title.data
            department.chief_id = form.chief_id.data
            department.members = form.members.data
            department.email = form.email.data
            db_sess.commit()
            return redirect("/departments")
        else:
            abort(404)
    return render_template("add_department.html", title="Изменить работу", form=form)


@app.route("/delete-department/<int:department_id>")
@login_required
def delete_department(department_id):
    db_sess = db_session.create_session()
    department = db_sess.query(Department).filter(Department.id == department_id) \
        .filter((Department.chief == current_user) | (current_user.id == 1)).first()
    if department:
        db_sess.delete(department)
        db_sess.commit()
    else:
        abort(404)
    return redirect("/departments")


@app.route("/departments")
def departments_log():
    db_sess = db_session.create_session()
    departments = db_sess.query(Department).all()
    return render_template("departments_log.html", departments=departments)


@app.route("/work-log")
def work_log():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).all()
    return render_template("work_log.html", jobs=jobs)


@app.route("/")
def index():
    return redirect("/work-log")


@app.errorhandler(404)
def not_found(_):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(400)
def bad_request(_):
    return make_response(jsonify({'error': 'Bad Request'}), 400)

@app.errorhandler(500)
def bad_request(error):
    return make_response(jsonify({'error': f'С сервером неполадки, я честно исправлю (нет), если что ошибка: {error}'}), 500)


def main():
    if not os.path.exists("db/blogs.db"):
        db_session.global_init("db/blogs.db")
        add_data_to_Base_of_Data()
    db_session.global_init("db/blogs.db")
    app.register_blueprint(jobs_api)
    init_api_routes(api)
    app.run("127.0.0.1", port=8000)


if __name__ == '__main__':
    main()