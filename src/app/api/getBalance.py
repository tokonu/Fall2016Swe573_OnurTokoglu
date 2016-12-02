from app import flask_app as app
from app import db
from flask_login import login_required, current_user
from flask import jsonify, request
from models.UserAteFood import UserAteFood
from models.UserDidActivity import UserDidActivity
from models.User import User
from datetime import datetime
from sqlalchemy import desc



@app.route('/userarea/getBalance', methods=['POST'])
@login_required
def getBalance():
    user = current_user  # type: User
    userId = user.user_id
    recommendedIntake = user.getRecommendedDailyIntake()

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

    results = db.session.query(UserAteFood).filter(UserAteFood.user_id == userId) \
        .filter(UserAteFood.date >= fromDate).filter(UserAteFood.date <= toDate).order_by(desc(UserAteFood.date)).all()

    balanceHist = {}

    for result in results:
        uafObj = result  # type: UserAteFood
        dateStr = datetime.strftime(uafObj.date, '%d-%m-%Y')
        dateReverse = datetime.strftime(uafObj.date, '%Y-%m-%d')
        if dateReverse not in balanceHist:
            balanceHist[dateReverse] = {
                "consumed": 0,
                "expended": 0,
                "recommended": recommendedIntake,
                "date": dateStr,
                "dateReverse": dateReverse
            }

        balanceHist[dateReverse]['consumed'] += uafObj.kcal

    results = db.session.query(UserDidActivity).filter(UserDidActivity.user_id == userId) \
        .filter(UserDidActivity.date >= fromDate).filter(UserDidActivity.date <= toDate)\
        .order_by(desc(UserDidActivity.date)).all()

    for result in results:
        udaObj = result  # type: UserDidActivity
        dateStr = datetime.strftime(udaObj.date, '%d-%m-%Y')
        dateReverse = datetime.strftime(udaObj.date, '%Y-%m-%d')
        if dateReverse not in balanceHist:
            balanceHist[dateReverse] = {
                "consumed": 0,
                "expended": 0,
                "recommended": recommendedIntake,
                "date": dateStr,
                "dateReverse": dateReverse
            }
        balanceHist[dateReverse]["expended"] += udaObj.kcal

    balanceList = []

    for dateReverse, histDict in balanceHist.items():
        if len(balanceList) == 0:
            balanceList.append(histDict)
            continue
        for i, sortedDict in enumerate(balanceList):
            if sortedDict["dateReverse"] > dateReverse:
                balanceList.insert(i, histDict)
                break
            elif i == len(balanceList)-1:
                balanceList.append(histDict)
                break

    return jsonify({"balanceHist": balanceList})









