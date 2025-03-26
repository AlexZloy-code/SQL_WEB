from datetime import datetime
import os

from flask import Flask, render_template, request

from data import db_session
from data.jobs import Jobs
from data.users import User
from forms.users import RegisterForm

app = Flask(__name__)
app.config["SECRET_KEY"] = "yandexlyceum_secret_key"


def get_users_data():
    users_data = [
        {
            "surname": "Scott",
            "name": "Ridley",
            "age": 21,
            "position": "captain",
            "speciality": "research engineer",
            "address": "module_1",
            "email": "scott_chief@mars.org",
        }
    ]
    return users_data


def create_users():
    db_sess = db_session.create_session()
    users = get_users_data()
    for user_data in users:
        user = User(**user_data)
        db_sess.add(user)
    db_sess.commit()


def get_jobs_data():
    jobs_data = [
        {
            "team_leader": 1,
            "job": "Deployment of residential modules 1 and 2",
            "work_size": 15,
            "collaborators": '',
            "start_date": datetime.now(),
            "is_finished": False,
        }
    ]
    return jobs_data


def create_jobs():
    db_sess = db_session.create_session()
    jobs = get_jobs_data()
    for job_data in jobs:
        job = Jobs(**job_data)
        db_sess.add(job)
    db_sess.commit()


def add_data_to_db():
    create_users()
    create_jobs()


@app.route("/")
def work_log():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).all()
    return render_template("work_log.html", jobs=jobs)


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.repeat_password.data:
            return render_template('register.html', title="Регистрация", messange='Пароли не совпадают')
        
        db_sess = db_session.create_session()

        user = User(
            surname=form.surname.data,
            name=form.name.data,
            age=form.age.data,
            position=form.position.data,
            speciality=form.speciality.data,
            address=form.address.data,
            email=form.login.data,
            hashed_password=form.password.data
        )

        db_sess.add(user)
        db_sess.commit()

        return 'Успешная регистрация'
    return render_template("register.html", title="Регистрация", form=form)



def main():
    if not os.path.exists('db/blogs.db'):
        add_data_to_db()
    
    db_session.global_init("db/blogs.db")
    app.run("127.0.0.1", port=8000)


if __name__ == '__main__':
    main()
