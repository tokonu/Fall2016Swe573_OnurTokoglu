from app import flask_app as app
from app import db
from flask_login import login_required, current_user
from flask import request
from app.login.RegisterForm import RegisterForm
from passlib.hash import sha256_crypt as hash
from app.models.WeightHist import WeightHist
import datetime


@app.route('/userarea/edituser', methods=['POST'])
@login_required
def editUser():
    newData = request.get_json()
    if "password" not in newData:
        newData["password"] = current_user.password
        print("password not in data")
    else:
        newData["password"] = hash.encrypt(newData["password"])
    if "email" not in newData:
        return "Invalid Request"
    form = RegisterForm(newData)
    error = form.validate

    if error is not None:
        return error

    if(current_user.weight != form.weight or current_user.height != form.height):
        weightHist = WeightHist(user_id=current_user.user_id, datetime=datetime.datetime.now() , weight=form.weight, height=form.height)
        db.session.add(weightHist)

    current_user.email = form.email
    current_user.password = form.password
    current_user.name = form.name
    current_user.birthday = form.birthday
    current_user.weight = form.weight
    current_user.height = form.height
    current_user.gender = form.gender
    current_user.notes = form.notes

    try:
        db.session.commit()
    except:
        db.session.rollback()
        return "Database error"

    return "ok"