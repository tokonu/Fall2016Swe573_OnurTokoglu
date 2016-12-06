from app import flask_app as app
from app import db
from flask_login import login_required, current_user
from flask import jsonify, request
from app.models.WeightHist import WeightHist
from datetime import datetime, timedelta

@app.route('/userarea/getWeightHistory', methods=['POST'])
@login_required
def getWeightHistory():
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
        toDate += timedelta(days=1) # weight field has datetime so any results
        # in toDate day is not returned, increment toDate by 1 day
    except:
        return jsonify(error="Enter birthday in DD-MM-YYYY format")

    results = db.session.query(WeightHist).filter(WeightHist.user_id == userId)\
        .filter(WeightHist.datetime >= fromDate).filter(WeightHist.datetime <= toDate).all()

    histList = []

    for result in results:
        weightObj = result  # type: WeightHist
        histList.append({
            "date": datetime.strftime(weightObj.datetime, '%d-%m-%Y'),
            "weight": weightObj.weight,
            "height": weightObj.height
        })

    print("returned weighthist " +str(len(histList)))
    return jsonify({"history":histList})