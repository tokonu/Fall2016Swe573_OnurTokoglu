from app import flask_app as app
from app import db
from flask_login import login_required
from flask import jsonify
from app.models.Activity import Activity


@app.route('/userarea/getActivities', methods=['POST', 'GET'])
@login_required
def getActivities():
    results = db.session.query(Activity).all()

    activityDict = {}

    for result in results:
        activityObj = result  # type: Activity
        activityDict[activityObj.id] = {
            "id" : activityObj.id,
            "name" : activityObj.name,
            "kcal_ph_pkg" : activityObj.kcal_ph_pkg,
            "duration" : 60
        }

    print("returned activities " + str(len(activityDict)))
    return jsonify({"activities": activityDict})