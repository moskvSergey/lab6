from flask import Flask, render_template, redirect, request, abort
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from data import db_session
from data.users import User
from data.jobs import Jobs
from data.departments import Departments
from forms.login import LoginForm
from forms.user import RegisterForm
from forms.jobs import JobsForm
from forms.departments import DepsForm


app = Flask(__name__)
app.config['SECRET_KEY'] = 'my_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)

@app.route("/")
def index():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).filter(Jobs.is_finished != True)
    deps = db_sess.query(Departments)
    # if current_user.is_authenticated:
    #     news = db_sess.query(News).filter(
    #         (News.user == current_user) | (News.is_private != True))
    # else:
    #     news = db_sess.query(News).filter(News.is_private != True)
    return render_template("index.html", jobs=jobs, deps=deps)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            email=form.email.data,
            name=form.name.data,
            last_name=form.last_name.data,
            age=form.age.data,
            position=form.position.data,
            speciality=form.speciality.data,
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/jobs',  methods=['GET', 'POST'])
@login_required
def add_jobs():
    form = JobsForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        jobs = Jobs()
        jobs.job = form.job.data
        jobs.work_size = form.work_size.data
        jobs.collaborators = form.collaborators.data

        jobs.team_leader = current_user.id
        db_sess.add(jobs)
        db_sess.commit()
        return redirect('/')
    return render_template('jobs.html', job='Добавление работы',
                           form=form)


@app.route('/jobs/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_jobs(id):
    form = JobsForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        jobs = db_sess.query(Jobs).filter(Jobs.id == id).first()
        if jobs:
            form.job.data = jobs.job
            form.work_size.data = jobs.work_size
            form.collaborators.data = jobs.collaborators
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        jobs = db_sess.query(Jobs).filter(Jobs.id == id).first()
        if jobs:
            jobs.job = form.job.data
            jobs.work_size = form.work_size.data
            jobs.collaborators = form.collaborators.data
            db_sess.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('jobs.html',
                           title='Редактирование работы',
                           form=form
                           )


@app.route('/jobs_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def jobs_delete(id):
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).filter(Jobs.id == id).first()
    if jobs:
        db_sess.delete(jobs)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')


@app.route('/deps',  methods=['GET', 'POST'])
@login_required
def add_deps():
    form = DepsForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        deps = Departments()
        deps.title = form.title.data
        deps.members = form.members.data
        deps.email = form.email.data

        db_sess.add(deps)
        db_sess.commit()
        return redirect('/')
    return render_template('departments.html', job='Добавление департамента',
                           form=form)


@app.route('/deps/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_deps(id):
    form = DepsForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        deps = db_sess.query(Departments).filter(Departments.id == id).first()
        if deps:
            form.title.data = deps.title
            form.members.data = deps.members
            form.email.data = deps.email
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        deps = db_sess.query(Departments).filter(Departments.id == id).first()
        if deps:
            deps.title = form.title.data
            deps.members = form.members.data
            deps.email = form.email.data
            db_sess.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('departments.html',
                           title='Редактирование департамента',
                           form=form
                           )


@app.route('/deps_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def deps_delete(id):
    db_sess = db_session.create_session()
    deps = db_sess.query(Departments).filter(Departments.id == id).first()
    if deps:
        db_sess.delete(deps)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')

def main():
    db_session.global_init("db/mars_explorer.db")
    app.run()


if __name__ == '__main__':
    main()