from app import db, login_manager
from app import flask_app as app
from flask import render_template, request, flash, url_for, redirect, abort, g, session
from flask_login import login_user, logout_user, current_user, login_required
from app.models.User import User
from passlib.hash import sha256_crypt as hash
from .RegisterForm import RegisterForm
from sqlalchemy import exc
from app.models.WeightHist import WeightHist
from datetime import datetime

@app.route('/')
def index():
    return redirect(url_for('userarea'))
    #return render_template('index.html')


@app.before_request
def before_request():
    g.user = current_user


@app.template_filter('dateddmmyyyy')
def _jinja2_filter_datetime(date, fmt=None):
    return date.strftime('%d-%m-%Y')


login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('userarea'))
    if request.method == 'GET':
        return render_template('login.html')

    email = request.form['email']
    password = request.form['password']

    if not email or not password:
        return render_template('login.html', err="Fill the form")

    try:
        registered_user = User.query.filter_by(email=email).first()
    except Exception as e:
        error_string = "Unknown error"
        if type(e) is exc.OperationalError:
            error_string = "Can't connect to mysql server"
        return render_template('login.html', err=error_string)

    if registered_user is None or not hash.verify(password, registered_user.password):
        return render_template('login.html', err="Wrong email or password")

    login_user(registered_user, remember=True)
    return redirect('userarea')


@app.route('/register', methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('userarea'))
    if request.method == 'GET':
        return render_template('register.html')

    form = RegisterForm(request.form)
    val_result = form.validate
    if val_result is not None:
        return render_template('register.html', err=val_result)

    user = User(form)
    user.password = hash.encrypt(user.password)
    user.birthday = datetime.strptime(user.birthday,'%d-%m-%Y') #for sqlite

    try:
        db.session.add(user)
        db.session.commit()
    except exc.IntegrityError as e:
        #the code below gives an error on sqlite
        #_, message = e.orig.args
        #db.session.rollback()
        #error_string = "Integrity error"
        #print(message)
        #if "Duplicate" in message and "email" in message:
        #    error_string = "Duplicate Email"
        return render_template('register.html', err="Duplicate email")
    except Exception as e:
        error_string = "Unknown error"
        print(e)
        if type(e) is exc.OperationalError:
            error_string = "Can't connect to mysql server"
        db.session.rollback()
        return render_template('register.html', err=error_string)

    weightHist = WeightHist(user_id=user.user_id, datetime=datetime.now(),
                            weight=user.weight, height=user.height)
    db.session.add(weightHist)
    try:
        db.session.add(weightHist)
        db.session.commit()
    except:
        db.session.rollback()
        pass

    login_user(user,remember=True)
    return redirect(url_for('userarea'))


@app.route('/userarea/')
@login_required
def userarea():
    return render_template('userarea.html')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))




















