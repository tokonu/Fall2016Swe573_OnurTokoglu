from app import flask_app as app
from app import db
from flask_login import login_required, current_user
from flask import jsonify, request
from models.UserDidActivity import UserDidActivity
from models.Activity import Activity
from datetime import datetime
from sqlalchemy import desc


@app.route('/userarea/getMyActivities', methods=['POST'])
@login_required
def getMyActivities():
    userId = current_user.user_id

    jsonReq = request.get_json()
    print(jsonReq)

    if not jsonReq:
        return jsonify(error="Request error")

    if 'from' not in jsonReq or 'to' not in jsonReq:
        return jsonify(error="Missing values")

    fromStr = jsonReq['from']
    toStr = jsonReq['to']

    try:
        fromDate = datetime.strptime(fromStr, '%d-%m-%Y')
        toDate = datetime.strptime(toStr, '%d-%m-%Y')
    except:
        return jsonify(error="Enter birthday in DD-MM-YYYY format")

    results = db.session.query(Activity, UserDidActivity).filter(UserDidActivity.activity_id == Activity.id)\
        .filter(UserDidActivity.user_id == userId).filter(UserDidActivity.date >= fromDate)\
        .filter(UserDidActivity.date <= toDate).order_by(desc(UserDidActivity.date)).all()

    actHist = []
    prevDate = ""
    index = -1

    for result in results:
        actObj = result[0]  # type: Activity
        udaObj = result[1]  # type: UserDidActivity
        dateStr = datetime.strftime(udaObj.date, '%d-%m-%Y')
        if prevDate != dateStr:
            prevDate = dateStr
            index += 1
            actHist.append({
                "date": dateStr,
                "activities": []
            })


        actDict = {
            "name": actObj.name,
            "duration": udaObj.duration_mnt,
            "kcal": udaObj.kcal,
            "entryId": udaObj.id
        }

        actHist[index]["activities"].append(actDict)

    print("my activities returned " + str(len(actHist)))

    return jsonify({"activityHist": actHist})




@app.route('/userarea/deleteActivityEntry', methods=['POST'])
@login_required
def deleteActivityEntry():

    jsonReq = request.get_json()
    # print(jsonReq)

    if not jsonReq:
        return jsonify(error="Request error")

    if "entryId" not in jsonReq:
        return jsonify(error="Missing values")

    entryId = jsonReq['entryId']

    db.session.query(UserDidActivity).filter(UserDidActivity.id == entryId).delete()

    try:
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify(error="Unknown error")

    return "ok"


















