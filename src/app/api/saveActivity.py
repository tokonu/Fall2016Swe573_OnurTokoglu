from app import flask_app as app
from app import db
from flask import request
from flask import jsonify
from flask_login import login_required, current_user
from models.UserDidActivity import UserDidActivity
from datetime import datetime

@app.route('/userarea/saveActivity', methods=['POST'])
@login_required
def saveActivity():
    activity = request.get_json()['activity']
    if not activity or 'id' not in activity or 'date' not in activity or 'duration' not in activity or 'kcal' not in activity:
        return jsonify(error="Missing values in request")

    try:
        date = datetime.strptime(activity['date'], '%d-%m-%Y')
    except:
        return jsonify(error="Enter birthday in DD-MM-YYYY format")

    userId = current_user.user_id
    userDidAct = UserDidActivity(activity["id"],userId,date,activity["kcal"],activity["duration"])

    try:
        db.session.add(userDidAct)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify(error=e)
    return "ok"